import re
import struct
import time

# --- 型態對應表 (C -> Python struct format) ---
CTYPE_TO_STRUCT = {
    "uint16_t": "H",
    "uint32_t": "I",
    "int16_t": "h",
    "int32_t": "i",
    "char": "s",  # 陣列處理特例
}


def parse_defines(filename="litelog.h"):
    """Parse #define LOG_LEVEL_xxx / LOG_DATA_TYPE_xxx"""
    levels = {}
    types = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            m1 = re.match(r"#define\s+LOG_LEVEL_([A-Za-z0-9_]+)\s+\((\d+)[Uu]?\)", line)
            if m1:
                name, val = m1.groups()
                if name != "ALL":
                    levels[int(val)] = name

            m2 = re.match(r"#define\s+LOG_DATA_TYPE_([A-Za-z0-9_]+)\s+\((\d+)[Uu]?\)", line)
            if m2:
                name, val = m2.groups()
                if name != "ALL":
                    types[int(val)] = name

    return levels, types


def parse_c_structs(filename="litelog.h"):
    """Parse typedef struct {...} NAME from C header and build LOG_SCHEMA"""
    schema = {}
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    struct_blocks = re.findall(
        r"typedef\s+struct\s*{([^}]*)}\s*([A-Za-z0-9_]+)",
        code,
        re.MULTILINE | re.DOTALL,
    )

    for idx, (block, name) in enumerate(struct_blocks):
        fields = []
        fmt = ""
        for line in block.splitlines():
            line = line.strip().rstrip(";")
            if not line:
                continue

            m = re.match(r"(\w+)\s+([A-Za-z0-9_]+)(\[(\d+)\])?", line)
            if not m:
                continue
            ctype, field, _, arrlen = m.groups()

            if ctype == "char" and arrlen:
                fmt += f"{arrlen}s"
            elif ctype in CTYPE_TO_STRUCT:
                fmt += CTYPE_TO_STRUCT[ctype]
            else:
                print(f"⚠️ 未知型態: {ctype}, 跳過欄位 {field}")
                continue

            fields.append(field)

        if fmt:
            schema[idx] = (fmt, fields, name)

    return schema


def parse_log(schema, levels, types, filename="log.bin"):
    """Parse log file using schema"""
    logs = []
    with open(filename, "rb") as f:
        while True:
            header = f.read(12)  # timestamp(4) + level(2) + type(2) + size(4)
            if not header:
                break
            if len(header) < 12:
                print("Corrupted header (too short)")
                break

            timestamp, level, ltype, data_size = struct.unpack("<IHHI", header)
            data = f.read(data_size)

            if len(data) != data_size:
                print(f"Warning: expected {data_size} bytes, got {len(data)}")
                break

            entry = {
                "log_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)),
                "log_level": levels.get(level, f"UNKNOWN({level})"),
                "log_type": types.get(ltype, f"UNKNOWN({ltype})"),
            }

            if ltype in schema:
                fmt, fields, cname = schema[ltype]
                expected_size = struct.calcsize("<" + fmt)
                if expected_size == data_size:
                    values = struct.unpack("<" + fmt, data)
                    for field, value in zip(fields, values):
                        if isinstance(value, (bytes, bytearray)):
                            value = value.split(b"\x00", 1)[0].decode(errors="ignore")
                        entry[field] = value
                else:
                    entry["raw"] = data.hex()
                    entry["note"] = f"Size mismatch: expected {expected_size}, got {data_size}"
            else:
                entry["raw"] = data.hex()

            logs.append(entry)
    return logs


if __name__ == "__main__":
    levels, types = parse_defines("litelog.h")
    schema = parse_c_structs("litelog.h")

    print("LOG_LEVELS =", levels)
    print("LOG_TYPES =", types)

    print("\n自動生成的 LOG_SCHEMA:")
    for idx, (fmt, fields, cname) in schema.items():
        print(f"  {idx}: ({fmt}, {fields})  # {cname}")

    print("\n解析 log.bin:")
    logs = parse_log(schema, levels, types, "log.bin")
    for i, log in enumerate(logs, 1):
        print(f"[{i}] {log}")

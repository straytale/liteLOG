import re
import struct
import time
import json

# --- C type to Python struct format mapping ---
CTYPE_TO_STRUCT = {
    "uint16_t": "H",
    "uint32_t": "I",
    "int16_t": "h",
    "int32_t": "i",
    "char": "s",  # arrays handled separately
}


def parse_defines(code: str, prefix: str):
    """
    Extract #define constants with a given prefix.
    Returns {int_value: name}.
    Skips *_MAX and *_ALL.
    """
    defines = {}
    for line in code.splitlines():
        m = re.match(rf"#define\s+{prefix}([A-Za-z0-9_]+)\s*\((\d+)[Uu]?\)", line)
        if m:
            name, val = m.groups()
            if name.upper() in ("MAX", "ALL"):
                continue
            defines[int(val)] = name
    return defines


def parse_structs(code: str):
    """
    Parse typedef struct definitions and build schema.
    Returns {index: (format, [field names], struct name)}
    """
    schema = {}
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
                continue

            fields.append(field)

        if fmt:
            schema[idx] = (fmt, fields, name)

    return schema


def parse_log(filename, log_levels, log_types, log_schema):
    """
    Parse the binary log file into structured Python dictionaries.
    """
    logs = []
    with open(filename, "rb") as f:
        while True:
            header = f.read(12)  # timestamp(4) + level(2) + type(2) + data_size(4)
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
                "log_level": log_levels.get(level, f"UNKNOWN({level})"),
                "log_type": log_types.get(ltype, f"UNKNOWN({ltype})"),
            }

            if ltype in log_schema:
                fmt, fields, _ = log_schema[ltype]
                expected_size = struct.calcsize("<" + fmt)
                if expected_size == data_size:
                    values = struct.unpack("<" + fmt, data)
                    for field, val in zip(fields, values):
                        if isinstance(val, (bytes, bytearray)):
                            val = val.split(b"\x00", 1)[0].decode(errors="ignore")
                        entry[field] = val
                else:
                    entry["raw"] = data.hex()
            else:
                entry["raw"] = data.hex()

            logs.append(entry)
    return logs


if __name__ == "__main__":
    # Load header
    with open("litelog.h", "r", encoding="utf-8") as f:
        code = f.read()

    # Parse levels, types, and structs
    log_levels = parse_defines(code, "LOG_LEVEL_")
    log_types = parse_defines(code, "LOG_DATA_TYPE_")
    log_schema = parse_structs(code)

    print("Detected log levels:", log_levels)
    print("Detected log types:", log_types)
    print("Detected schema:")
    for idx, (fmt, fields, name) in log_schema.items():
        print(f"  {idx}: {name} -> format='{fmt}', fields={fields}")

    # Parse log file
    logs = parse_log("log.bin", log_levels, log_types, log_schema)

    # Print logs to console
    for i, log in enumerate(logs, 1):
        print(f"[{i}] {log}")

    # Save logs to JSON
    with open("log.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

    print(f"\nSaved {len(logs)} logs to log.json")

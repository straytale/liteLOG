# 📒 LiteLog
### 輕量級日誌紀錄與解析工具

這是一個簡單的 **C 語言日誌紀錄程式庫**，搭配 Python 腳本可以解析與檢視 log 資料。  
適合嵌入式環境或需要低成本日誌功能的應用。

---

## 🗂️ 專案結構
- `litelog.h`  
  - 提供日誌紀錄相關的函式定義，使用者可自行定義事件類型、資料結構
- `test.c`  
  - 範例程式，示範如何記錄日誌
- `parser.py`  
  - Python 腳本，解析日誌檔案並轉換成 json 格式

---

## 💡 想法
相較於傳統的 `printf` 除錯方式，往往難以直接輸出 **struct 結構**，  
LiteLog 定義出一套 **結構化日誌輸出框架**，並搭配 Python 腳本進行解析。  

開發者可以自行定義 **log data types** 與對應的 **struct**，例如：

```c
#define LOG_DATA_TYPE_EXAMPLE1 (1U) // user-defined log data type

typedef struct // user-defined data structure
{
    uint16_t cpu_usage; // MAX to 0x64
    uint16_t mem_usage; // MAX to 0x64
    uint32_t thread_count;
} LOG_DATA_EXAMPLE1, *LOG_DATA_EXAMPLE1_PTR;
#define LOG_DATA_TYPE_EXAMPLE1_SIZE (sizeof(LOG_DATA_EXAMPLE1))
```

並在程式中加入自訂 log：

```c
LOG_DATA_EXAMPLE1 example1 = {
    .cpu_usage = 45,
    .mem_usage = 30,
    .thread_count = 5
}; // 範例數值

ADD_LOG(
    LOG_LEVEL_WARNING,
    LOG_DATA_TYPE_EXAMPLE1, // user-defined log data types
    LOG_ACTION_NONE,        // action: NONE or SAVE_NOW
    &example1,              // user-defined data structure
    LOG_DATA_TYPE_EXAMPLE1_SIZE
);
```
其中，LOG_ACTION分成NONE與SAVE_NOW，前者會等到可用entries滿的時候，自動生成log檔案，而後者是立即生成，在生成log之後，會立即清空entries

這樣便能將複雜的結構化資料直接寫入 log 檔，再透過 Python 解析器轉換為 JSON，方便後續檢視與分析。  

---

## 🚀 使用方式

### 1. 編譯與執行範例程式
```bash
gcc test.c -o test
./test
```

執行後會輸出一份二進位日誌檔 `log.bin`。

---

### 2. 使用 Python 解析器
```bash
python3 parser.py -f log.bin
```

可將日誌轉換成JSON格式，方便檢視。

---

### 3. 輸出範例
```bash
[
    {
        "log_time": "2025-09-13 10:41:57",
        "log_level": "WARNING",
        "log_type": "EXAMPLE1",
        "cpu_usage": 45,
        "mem_usage": 30,
        "thread_count": 5
    },
    {
        "log_time": "2025-09-13 10:41:57",
        "log_level": "ERROR",
        "log_type": "EXAMPLE2",
        "src_ip": "10.0.0.1",
        "dst_ip": "8.8.8.8",
        "port": 8080
    },
    {
        "log_time": "2025-09-13 10:41:57",
        "log_level": "FATAL",
        "log_type": "EXAMPLE3",
        "name": "TestUser",
        "level": 1
    },
    {
        "log_time": "2025-09-13 10:41:57",
        "log_level": "INFO",
        "log_type": "MSG",
        "msg": "This is a test log message.\n\r"
    }
]
```

日誌會轉換成 JSON 格式，方便檢視。

---

## 📝 功能特色
- 輕量結構，適合嵌入式裝置  
- 支援等級分類（INFO / WARNING / ERROR / FATAL）  
- 使用 Python 腳本快速解析  
- 簡單易於整合  

---

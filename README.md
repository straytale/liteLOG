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
  - Python 腳本，解析日誌檔案並轉換成json格式

---

## 🚀 使用方式

### 1. 編譯與執行範例程式
```bash
gcc test.c -o test
./test
```

執行後會輸出一份二進位日誌檔。

---

### 2. 使用 Python 解析器
```bash
python3 parser.py -f <log_file>
```

可將日誌轉換成人類可讀的格式，方便檢視。

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

可將日誌轉換成json格式，方便檢視。

---

## 📝 功能特色
- 輕量結構，適合嵌入式裝置  
- 支援等級分類（INFO / WARNING / ERROR / FATAL）  
- 使用 Python 腳本快速解析  
- 簡單易於整合  

---


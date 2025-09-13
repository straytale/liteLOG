# 📒 LiteLog
### 副標題：輕量級日誌紀錄與解析工具

這是一個簡單的 **C 語言日誌紀錄程式庫**，搭配 Python 腳本可以解析與檢視 log 資料。  
適合嵌入式環境或需要低成本日誌功能的應用。

---

## 🗂️ 專案結構
- `litelog.h`  
  - 提供日誌紀錄相關的結構與函式定義  
- `test.c`  
  - 範例程式，示範如何記錄與輸出日誌  
- `parser.py`  
  - Python 腳本，解析日誌檔案並轉換成可讀格式  

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
python3 parser.py <log_file>
```

可將日誌轉換成人類可讀的格式，方便檢視。

---

## 📝 功能特色
- 輕量結構，適合嵌入式裝置  
- 支援等級分類（Normal / Warning / Error / Debug …）  
- 使用 Python 腳本快速解析  
- 簡單易於整合  

---

## 📊 範例
C 程式寫入日誌：
```c
log_entry entry;
entry.level = 1;  // warning
entry.assignee = 3;
entry.data_size = sizeof("Hello");
entry.data = "Hello";
```

Python 解析後輸出：
```text
[2025-09-13 10:30:12] [WARNING] (assignee=3) Hello
```

---
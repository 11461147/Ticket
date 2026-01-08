# 拓元搶票機器人 

自動化拓元售票系統 (tixcraft.com) 的搶票工具，使用 Python + Selenium + ddddocr 實現全自動搶票流程。

##  功能特色

-  **全自動搶票流程**：從場次選擇到最終提交一氣呵成
-  **智能場次選擇**：支援關鍵字匹配或自動選擇第一個可用場次
-  **純 JS 快速選位**：使用 JavaScript 一次性執行選位，速度提升 10-50 倍
-  **智能座位篩選**：自動跳過剩餘數量不足的區域
-  **自動勾選條款**：自動處理所有必要的 checkbox
-  **AI 驗證碼識別**：使用 ddddocr 自動識別並填入驗證碼（最多重試 2 次）
-  **設定自動儲存**：輸入內容自動保存，下次啟動自動載入
-  **智能路由系統**：自動偵測頁面狀態，失敗時自動重整重試
-  **防偵測機制**：停用自動化特徵，降低被封鎖機率

##  系統需求

- Python 3.7+
- Chrome 瀏覽器
- Selenium 4.6+（自動下載 ChromeDriver）

##  快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 運行程式

```bash
python tixcraft.py
```

> **注意**：程式使用 Selenium 4.6+ 的 selenium-manager 自動下載對應版本的 ChromeDriver，無需手動設定！

##  使用說明

### 基本操作

1. **啟動程式**：執行 `python tixcraft.py`，開啟 GUI 介面
2. **填入搶票網址**：輸入拓元活動頁面網址
3. **設定場次關鍵字**（可選）：輸入場次關鍵字，留空則自動選擇第一個
4. **設定購票張數**：輸入 1-4 的數字
5. **點擊開始搶票**：程式會開啟 Chrome 到拓元首頁
6. **手動登入**：在開啟的瀏覽器中登入你的拓元帳號
7. **進入搶票頁面**：程式會自動偵測並開始搶票流程

### 搶票流程

```

  開啟首頁  手動登入  進入活動頁                        
                                                        
  自動選擇場次  純JS快速選位  確認座位                  
                                                        
  填寫購票資料  AI識別驗證碼  自動提交                  
                                                        
  失敗自動重試 / 成功完成購票                             

```

##  設定檔

程式會自動創建 `tixcraft_config.json` 保存你的設定：

```json
{
  "url": "搶票網址",
  "session": "場次關鍵字",
  "ticket_count": "1"
}
```

##  進階設定

### 時間參數（在 tixcraft.py 開頭）

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `POLL_INTERVAL_MS` | 100ms | 路由輪詢間隔 |
| `AREA_REFRESH_INTERVAL_MS` | 2000ms | 選位失敗時重整間隔 |
| `CAPTCHA_MAX_ATTEMPTS` | 2 | 驗證碼最大嘗試次數 |
| `REFRESH_ON_AREA` | True | 選位失敗時是否自動重整 |

### 選位邏輯

程式會自動篩選座位區域：
-  可點擊的區域
-  剩餘數量  購票張數
-  已售完 / disabled / 不可見

##  注意事項

- 請確保在合理範圍內使用，遵守網站服務條款
- 建議在正式搶票前先測試流程
- 網站更新可能需要調整選擇器
- 驗證碼識別率約 80-90%，偶爾需要手動輸入

##  常見問題

### ChromeDriver 相關

**Q: ChromeDriver 啟動失敗**
A: 程式使用 Selenium 4.6+ 自動管理 ChromeDriver，請確保 Selenium 版本正確：
```bash
pip install --upgrade selenium
```

**Q: Chrome 版本不匹配**
A: 更新 Chrome 瀏覽器到最新版本

### 搶票相關

**Q: 找不到場次按鈕**
A: 檢查場次關鍵字是否正確，或留空讓程式自動選擇第一個可用場次

**Q: 選位一直重整**
A: 可能所有區域都已售完或剩餘數量不足，程式會持續重整等待釋票

**Q: 驗證碼識別失敗**
A: ddddocr 對某些驗證碼識別率較低，超過 2 次失敗後會交回路由重試

##  檔案結構

```
Ticket/
 tixcraft.py           # 主程式
 tixcraft_config.json  # 設定檔（自動生成）
 tixcraft_架構說明.md   # 程式架構文件
 requirements.txt      # Python 依賴
 README.md             # 本文件
 tools/
     download_chromedriver.py  # ChromeDriver 下載工具（可選）
```

##  授權條款

本專案僅供學習研究使用，請勿用於商業用途。

---

 如果這個專案對你有幫助，請給個星星支持一下！

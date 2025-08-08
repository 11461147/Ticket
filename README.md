# 拓元搶票機器人 🎫

自動化拓元售票系統的搶票工具，使用 Python + Selenium 實現全自動搶票流程。

## ✨ 功能特色

- 🚀 **全自動搶票流程**：從場次選擇到最終提交
- 🎯 **智能場次選擇**：支援關鍵字匹配或自動選擇第一個可用場次
- 💺 **自動選位**：自動選擇可用座位區域
- 🔢 **購票張數設定**：支援 1-4 張票數選擇
- ✅ **自動勾選條款**：自動處理所有必要的 checkbox
- 🔍 **AI 驗證碼識別**：使用 ddddocr 自動識別並填入驗證碼
- 💾 **設定自動儲存**：輸入內容自動保存，下次啟動自動載入
- ⚡ **智能等待機制**：基於元素載入狀態，不使用固定延遲

## 📋 系統需求

- Python 3.7+
- Chrome 瀏覽器
- ChromeDriver

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 下載 ChromeDriver

從 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下載對應版本的 ChromeDriver

### 3. 設定 Chrome 路徑

修改 `tixcraft.py` 中的 Chrome 和 ChromeDriver 路徑：

```python
chromedriver_path = r"你的ChromeDriver路徑"
options.binary_location = r"你的Chrome路徑"
```

### 4. 運行程式

```bash
python tixcraft.py
```

## 📖 使用說明

### 基本操作

1. **啟動程式**：執行 `python tixcraft.py`
2. **填入搶票網址**：輸入拓元活動頁面網址
3. **設定場次關鍵字**（可選）：輸入場次關鍵字，留空則自動選擇第一個
4. **設定購票張數**：輸入 1-4 的數字
5. **點擊開始搶票**：程式會開啟瀏覽器到拓元首頁
6. **手動登入**：在開啟的瀏覽器中登入帳號
7. **進入搶票頁面**：程式會自動檢測並開始搶票流程

### 搶票流程

```
開啟首頁 → 手動登入 → 進入搶票頁面 → 自動選擇場次 → 自動選位 → 
自動填寫購票資料 → AI識別驗證碼 → 自動提交表單
```

## ⚙️ 設定檔

程式會自動創建 `tixcraft_config.json` 保存你的設定：

```json
{
  "url": "搶票網址",
  "session": "場次關鍵字", 
  "ticket_count": "購票張數"
}
```

## 🔧 進階設定

### 調整等待時間

可以修改程式中的 `WebDriverWait` 超時時間：

```python
WebDriverWait(self.driver, 15)  # 15秒超時
```

### 自定義選擇器

可以修改各種元素的 CSS 選擇器來適應網站變化。

## ⚠️ 注意事項

- 請確保在合理範圍內使用，遵守網站服務條款
- 建議在測試環境先試運行
- 網站更新可能需要調整選擇器
- 使用前請確保已登入拓元帳號

## 🐛 常見問題

### ChromeDriver 相關

**Q: ChromeDriver 版本不匹配**
A: 確保 ChromeDriver 版本與 Chrome 瀏覽器版本一致

**Q: 找不到 ChromeDriver**  
A: 檢查路徑設定是否正確，或將 ChromeDriver 加入系統 PATH

### 搶票相關

**Q: 找不到場次按鈕**
A: 檢查場次關鍵字是否正確，或留空讓程式自動選擇

**Q: 驗證碼識別失敗**
A: ddddocr 對某些驗證碼類型識別率較低，可能需要手動處理

## 📄 授權條款

本專案僅供學習研究使用，請勿用於商業用途。

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善這個專案！

---

⭐ 如果這個專案對你有幫助，請給個星星支持一下！
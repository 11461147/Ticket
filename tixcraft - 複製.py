

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os

# Selenium imports
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class TixcraftGUI:
    def __init__(self, root):
        self.root = root
        root.title("拓元搶票機器人")
        root.geometry("400x600")
        
        # 設定檔路徑
        self.config_file = "tixcraft_config.json"
        
        # 載入設定
        self.load_config()

        # 搶票網址
        tk.Label(root, text="搶票網址:").pack(anchor='w', padx=10, pady=(10, 0))
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(padx=10, pady=5)
        self.url_entry.bind('<KeyRelease>', self.on_config_change)

        # LOG紀錄區（移到網址下方）
        tk.Label(root, text="LOG紀錄:").pack(anchor='w', padx=10, pady=(10, 0))
        self.log_text = scrolledtext.ScrolledText(root, width=48, height=15, state='disabled')
        self.log_text.pack(padx=10, pady=5)

        # 場次選擇輸入框
        tk.Label(root, text="購票場次:").pack(anchor='w', padx=10, pady=(10, 0))
        self.session_entry = tk.Entry(root, width=30)
        self.session_entry.pack(padx=10, pady=5)
        self.session_entry.bind('<KeyRelease>', self.on_config_change)

        # 購票張數輸入框
        tk.Label(root, text="購票張數(1-4):").pack(anchor='w', padx=10, pady=(10, 0))
        self.ticket_count_entry = tk.Entry(root, width=10)
        self.ticket_count_entry.pack(padx=10, pady=5)
        self.ticket_count_entry.bind('<KeyRelease>', self.on_config_change)

        # 開始/暫停搶票按鈕
        self.is_running = False
        self.start_btn = tk.Button(root, text="開始搶票", command=self.toggle_ticketing)
        self.start_btn.pack(padx=10, pady=10)
        
        # 填入之前儲存的值
        self.apply_config()
        
        # 視窗關閉時自動儲存
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """載入設定檔"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self.log_message("已載入設定檔")
            else:
                self.config = {
                    "url": "",
                    "session": "",
                    "ticket_count": "1"
                }
        except Exception as e:
            self.config = {
                "url": "",
                "session": "",
                "ticket_count": "1"
            }
            self.log_message(f"載入設定檔失敗: {e}")

    def save_config(self):
        """儲存設定檔"""
        try:
            self.config = {
                "url": self.url_entry.get(),
                "session": self.session_entry.get(),
                "ticket_count": self.ticket_count_entry.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"儲存設定檔失敗: {e}")

    def apply_config(self):
        """將設定套用到GUI"""
        self.url_entry.insert(0, self.config.get("url", ""))
        self.session_entry.insert(0, self.config.get("session", ""))
        self.ticket_count_entry.insert(0, self.config.get("ticket_count", "1"))

    def on_config_change(self, event=None):
        """當設定改變時自動儲存"""
        self.save_config()

    def on_closing(self):
        """視窗關閉時的處理"""
        self.save_config()
        self.root.destroy()

    def log_message(self, message):
        """用於內部LOG（避免在初始化時調用log方法）"""
        print(message)

    def toggle_ticketing(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="暫停搶票")
            self.start_ticketing()
        else:
            self.is_running = False
            self.start_btn.config(text="開始搶票")
            self.log("已暫停搶票。")
    def start_ticketing(self):
        # 啟動 Selenium ChromeDriver，只開首頁，等待用戶手動進入指定網址
        from selenium.webdriver.support import expected_conditions as EC
        import time
        import os

        url = self.url_entry.get().strip()
        if not url:
            url = "https://tixcraft.com/"
        self.log(f"僅開啟首頁，請手動進入搶票頁面：{url}")

        try:
            import tempfile, shutil
            chromedriver_path = r"C:\Users\user\Downloads\chrome-win64\chrome-win64\chromedriver.exe"
            options = webdriver.ChromeOptions()
            options.add_experimental_option('detach', True)
            # 自動產生唯一user-data-dir避免衝突
            self._user_data_dir = tempfile.mkdtemp(prefix="tixcraft_profile_")
            options.add_argument(f'--user-data-dir={self._user_data_dir}')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.binary_location = r"C:\Users\user\Downloads\chrome-win64\chrome-win64\chrome.exe"
            service = Service(chromedriver_path, port=9515)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get("https://tixcraft.com/")
            self.log("已開啟拓元首頁，請自行登入與進入搶票頁面。")
            self.monitor_url = url
            self.after_id = None
            self._wait_for_target_url()
        except Exception as e:
            self.log(f"ChromeDriver 啟動失敗: {e}")


    def _wait_for_target_url(self):
        # 定時檢查目前driver網址，若到達目標網址才觸發搶票流程
        if not self.is_running:
            return
        try:
            current_url = self.driver.current_url
            # 若進入detail頁自動跳轉game頁
            if "/activity/detail/" in current_url:
                game_url = current_url.replace("/detail/", "/game/")
                self.log(f"偵測到detail頁，自動導向 {game_url}")
                self.driver.get(game_url)
                # 重新檢查是否到達目標
                current_url = self.driver.current_url
            # 判斷是否為game頁（包含/activity/game/）
            if "/activity/game/" in current_url:
                self.log("已進入目標頁面，開始自動搶票流程！")
                self._auto_ticketing()
                return
        except Exception as e:
            self.log(f"瀏覽器檢查失敗: {e}")
            return
        # 每0.1秒檢查一次，更快響應
        if self.is_running:
            self.after_id = self.log_text.after(100, self._wait_for_target_url)

    def _auto_ticketing(self):
        # 每個 tr.gridc.fcTxt 只會有一個 button，直接比對關鍵字或點第一個
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.gridc.fcTxt'))
            )
            rows = self.driver.find_elements(By.CSS_SELECTOR, 'tr.gridc.fcTxt')
            self.log(f'找到 {len(rows)} 個場次')
            session_keyword = self.session_entry.get().strip()
            found = False
            for i, row in enumerate(rows):
                row_text = row.text
                self.log(f'場次 {i+1}: {row_text}')
                try:
                    btn = row.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
                    self.log(f'按鈕enabled狀態: {btn.is_enabled()}')
                    if not btn.is_enabled():
                        self.log(f'場次 {i+1} 按鈕disabled，跳過')
                        continue
                    # 有關鍵字時只點包含該關鍵字的場次
                    if session_keyword:
                        if session_keyword in row_text:
                            self.log(f'找到可購票按鈕（場次: {row_text}），用JS點擊...')
                            self.driver.execute_script("arguments[0].click();", btn)
                            self.log('JS點擊完成，等待跳轉選位頁面...')
                            # 直接等待選位頁面元素載入，不用固定時間等待
                            self._handle_seat_selection()
                            found = True
                            break
                    else:
                        # 沒有關鍵字直接點第一個
                        self.log(f'未輸入關鍵字，自動點擊第一個可購票按鈕（場次: {row_text}）')
                        self.driver.execute_script("arguments[0].click();", btn)
                        self.log('JS點擊完成，等待跳轉選位頁面...')
                        # 直接等待選位頁面元素載入，不用固定時間等待
                        self._handle_seat_selection()
                        found = True
                        break
                except Exception as e:
                    self.log(f'場次 {i+1} 找不到按鈕: {e}')
            if not found:
                self.log('未找到可購票按鈕，可能已售完、尚未開放或關鍵字不符。')
        except Exception as e:
            self.log(f'自動搶票流程錯誤: {e}')

    def _handle_seat_selection(self):
        # 處理選位頁面的自動化 - 等待頁面載入完成後立即動作
        if not self.is_running:
            return
        try:
            # 等待選位頁面完全載入
            self.log('等待選位頁面載入...')
            WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.url_contains("/ticket/area/"),
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.zone.area-list'))
                )
            )
            
            current_url = self.driver.current_url
            self.log(f'選位頁面URL: {current_url}')
            
            # 檢查是否在選位頁面（包含area字樣）
            if "/ticket/area/" in current_url:
                self.log('已進入選位頁面，開始自動選位...')
                
                # 等待選位區域元素載入
                try:
                    area_list_div = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.zone.area-list'))
                    )
                    a_tags = area_list_div.find_elements(By.TAG_NAME, 'a')
                    self.log(f'找到 {len(a_tags)} 個可購買座位區域')
                    
                    if a_tags:
                        # 點擊第一個找到的<a>標籤
                        first_a = a_tags[0]
                        area_text = first_a.text or first_a.get_attribute('title') or '未知區域'
                        self.log(f'點擊座位區域: {area_text}')
                        self.driver.execute_script("arguments[0].click();", first_a)
                        self.log('座位區域選擇完成')
                        
                        # 直接等待確認按鈕出現並處理
                        self._confirm_selection()
                    else:
                        self.log('沒有找到可購買的座位區域')
                        
                except Exception as e:
                    self.log(f'選位區域搜尋錯誤: {e}')
            else:
                # 還沒跳轉，重新檢查
                self.log('尚未跳轉到選位頁面，重新嘗試...')
                self.after_id = self.log_text.after(1000, self._handle_seat_selection)
        except Exception as e:
            self.log(f'選位頁面處理錯誤: {e}')

    def _confirm_selection(self):
        # 確認選位並進入下一步 - 等待確認按鈕載入後立即點擊
        if not self.is_running:
            return
        try:
            self.log('等待確認按鈕載入...')
            
            # 等待確認按鈕出現
            confirm_btn = WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[onclick*="confirm"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"][value*="確認"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="button"][value*="確認"]')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary')),
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[onclick*="confirm"]'))
                )
            )
            
            btn_text = confirm_btn.text or confirm_btn.get_attribute('value') or ''
            self.log(f'找到確認按鈕: {btn_text}')
            
            # 確認按鈕文字是否包含相關關鍵字
            if any(keyword in btn_text for keyword in ['確認', '下一步', '繼續', 'confirm', 'next']):
                self.log('點擊確認按鈕...')
                self.driver.execute_script("arguments[0].click();", confirm_btn)
                self.log('選位確認完成！')
                # 直接等待購票表單頁面載入
                self._handle_ticket_form()
            else:
                self.log('按鈕文字不符合確認條件，重新尋找...')
                self.after_id = self.log_text.after(1000, self._confirm_selection)
                
        except Exception as e:
            self.log(f'確認選位錯誤: {e}')
            # 重試
            self.after_id = self.log_text.after(2000, self._confirm_selection)

    def _handle_ticket_form(self):
        # 處理購票資料填寫頁面 - 等待表單元素載入完成後立即處理
        if not self.is_running:
            return
        try:
            # 等待購票表單頁面完全載入
            self.log('等待購票表單頁面載入...')
            WebDriverWait(self.driver, 15).until(
                EC.any_of(
                    EC.url_contains("/ticket/ticket/"),
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name*="ticketPrice"], select[id*="ticketPrice"]')),
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))
                )
            )
            
            current_url = self.driver.current_url
            self.log(f'購票資料頁面URL: {current_url}')
            self.log('購票表單已載入完成，開始處理購票資料填寫...')
            
            # 1. 處理張數下拉選單
            ticket_count = self.ticket_count_entry.get().strip()
            if not ticket_count or not ticket_count.isdigit():
                ticket_count = "1"
            self.log(f'設定購票張數: {ticket_count}')
            
            try:
                # 等待下拉選單載入
                select_elements = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select[name*="ticketPrice"], select[id*="ticketPrice"]'))
                )
                for select in select_elements:
                    try:
                        # 尋找對應張數的option
                        options = select.find_elements(By.TAG_NAME, 'option')
                        for option in options:
                            if option.get_attribute('value') == ticket_count:
                                self.log(f'選擇張數選項: {option.text}')
                                option.click()
                                break
                    except Exception as e:
                        self.log(f'下拉選單操作錯誤: {e}')
            except Exception as e:
                self.log(f'找不到張數下拉選單: {e}')
            
            # 2. 安全地處理checkbox - 等待載入後再處理
            try:
                checkboxes = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))
                )
                self.log(f'找到 {len(checkboxes)} 個checkbox')
                for i, checkbox in enumerate(checkboxes):
                    try:
                        # 檢查checkbox是否可見且可點擊
                        if checkbox.is_displayed() and checkbox.is_enabled() and not checkbox.is_selected():
                            # 先嘗試讓checkbox可見
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                            # 使用JS點擊更安全
                            self.driver.execute_script("arguments[0].click();", checkbox)
                            self.log(f'勾選checkbox {i+1}')
                        elif checkbox.is_selected():
                            self.log(f'checkbox {i+1} 已勾選')
                        else:
                            self.log(f'checkbox {i+1} 不可勾選 (disabled或不可見)')
                    except Exception as e:
                        self.log(f'checkbox {i+1} 處理失敗: {str(e)[:50]}...')
            except Exception as e:
                self.log(f'checkbox處理錯誤: {e}')
            
            # 3. 直接等待驗證碼圖片載入並處理
            self.log('開始處理驗證碼...')
            self._handle_captcha()
            
        except Exception as e:
            self.log(f'購票資料頁面處理錯誤: {e}')

    def _handle_captcha(self):
        # 使用ddddocr處理驗證碼
        if not self.is_running:
            return
        try:
            self.log('開始尋找驗證碼圖片...')
            
            # 使用更全面的等待策略確保驗證碼圖片完全載入
            try:
                # 先等待任何驗證碼相關圖片出現
                captcha_img = WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[style*="cursor:pointer"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="verify"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt*="驗證"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[id*="captcha"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[class*="captcha"]'))
                    )
                )
                self.log(f'找到驗證碼圖片元素: {captcha_img.get_attribute("src") or "無src屬性"}')
                
                # 等待圖片完全載入且可見
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of(captcha_img)
                )
                self.log('驗證碼圖片已可見')
                
                # 額外等待確保圖片內容載入完成
                WebDriverWait(self.driver, 5).until(
                    lambda driver: captcha_img.get_attribute('naturalWidth') != '0'
                )
                self.log('驗證碼圖片載入完成，開始識別...')
                
            except Exception as e:
                self.log(f'等待驗證碼圖片失敗: {e}')
                # 如果找不到驗證碼圖片，重試一次
                self.log('1秒後重試尋找驗證碼...')
                self.after_id = self.log_text.after(1000, self._handle_captcha)
                return
            
            # 截取驗證碼圖片
            import base64
            import io
            from PIL import Image
            
            # 獲取圖片的base64數據
            img_base64 = self.driver.execute_script("""
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var img = arguments[0];
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                ctx.drawImage(img, 0, 0);
                return canvas.toDataURL('image/png').split(',')[1];
            """, captcha_img)
            
            # 使用ddddocr識別
            try:
                import ddddocr
                ocr = ddddocr.DdddOcr()
                img_bytes = base64.b64decode(img_base64)
                captcha_text = ocr.classification(img_bytes)
                self.log(f'驗證碼識別結果: {captcha_text}')
                
                # 等待驗證碼輸入框載入並填入
                try:
                    captcha_input = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name*="verify"], input[id*="verify"], input[placeholder*="驗證"]'))
                    )
                    captcha_input.clear()
                    captcha_input.send_keys(captcha_text)
                    self.log('驗證碼已填入，立即提交...')
                    
                    # 驗證碼填入後立即提交
                    self._submit_form()
                except Exception as e:
                    self.log(f'驗證碼輸入框處理錯誤: {e}')
                    
            except ImportError:
                self.log('請先安裝ddddocr: pip install ddddocr')
            except Exception as e:
                self.log(f'驗證碼識別錯誤: {e}')
                
        except Exception as e:
            self.log(f'驗證碼處理錯誤: {e}')

    def _submit_form(self):
        # 提交購票表單
        if not self.is_running:
            return
        try:
            self.log('尋找提交按鈕...')
            # 修正CSS選擇器，移除 :contains() 因為Selenium不支援
            submit_selectors = [
                'button.btn.btn-primary.btn-green',  # 確認張數按鈕（綠色）
                'button[type="submit"].btn-green',
                'input[type="submit"]',
                'button[type="submit"]',
                'input[value*="確認"]',
                'input[value*="提交"]',
                'input[value*="下一步"]',
                'button[onclick*="submit"]',
                'input[onclick*="submit"]',
                'button.btn-green'  # 通用綠色按鈕
            ]
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn_text = btn.text or btn.get_attribute('value') or ''
                            self.log(f'找到提交按鈕: {btn_text} (選擇器: {selector})')
                            submit_btn = btn
                            break
                    if submit_btn:
                        break
                except Exception as e:
                    self.log(f'選擇器 {selector} 錯誤: {e}')
                    continue
            
            if submit_btn:
                self.driver.execute_script("arguments[0].click();", submit_btn)
                self.log('表單提交完成！搶票流程結束。')
            else:
                self.log('未找到提交按鈕')
            
        except Exception as e:
            self.log(f'表單提交錯誤: {e}')

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = TixcraftGUI(root)
    root.mainloop()

# 簡單腳本：使用 webdriver-manager 下載對應的 chromedriver 並複製到專案的 chromedriver 資料夾
from webdriver_manager.chrome import ChromeDriverManager
import shutil
import os
import sys

try:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dst_dir = os.path.join(base_dir, 'chromedriver-win64', 'chromedriver-win64')
    os.makedirs(dst_dir, exist_ok=True)

    print('開始下載 chromedriver...')
    driver_path = ChromeDriverManager().install()
    print('下載完成，來源：', driver_path)

    dst_path = os.path.join(dst_dir, 'chromedriver.exe')
    shutil.copy(driver_path, dst_path)
    print('已複製到：', dst_path)
    sys.exit(0)
except Exception as e:
    print('下載或複製失敗：', e)
    sys.exit(2)

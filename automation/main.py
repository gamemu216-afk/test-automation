"""
Test Automation Tool - Main Script
Tool tự động test website với Selenium
"""

import os
import sys
import time
import random
import logging
import csv
from datetime import datetime
from pathlib import Path

# Thêm thư mục automation vào path
sys.path.insert(0, os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from openpyxl import load_workbook
import config

# Setup logging
if config.LOG_ACTIONS:
    logging.basicConfig(
        filename=config.LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class TestAutomation:
    def __init__(self):
        self.driver = None
        self.results = []
        self.setup_browser()
        
    def setup_browser(self):
        """Thiết lập Chrome browser"""
        chrome_options = Options()
        
        if config.HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument(f"--window-size={config.BROWSER_WINDOW_SIZE[0]},{config.BROWSER_WINDOW_SIZE[1]}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent spoofing
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59'
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        logger.info("Browser setup completed")
        
    def random_delay(self, min_delay=None, max_delay=None):
        """Delay ngẫu nhiên giữa các thao tác"""
        min_d = min_delay or config.MIN_DELAY
        max_d = max_delay or config.MAX_DELAY
        delay = random.uniform(min_d, max_d)
        logger.info(f"Waiting {delay:.2f} seconds...")
        print(f"⏳ Chờ {delay:.2f} giây...")
        time.sleep(delay)
        
    def random_scroll(self):
        """Scroll ngẫu nhiên trên trang"""
        try:
            scroll_amount = random.randint(3, 8)
            for _ in range(scroll_amount):
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(random.uniform(0.5, 2))
            logger.info("Random scroll completed")
        except Exception as e:
            logger.error(f"Scroll error: {e}")
    
    def human_like_typing(self, element, text):
        """Gõ chữ giống con người (không quá nhanh)"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        logger.info(f"Typed: {text}")
        
    def read_keywords_from_excel(self):
        """Đọc từ khóa từ file Excel"""
        try:
            if not os.path.exists(config.EXCEL_FILE):
                logger.error(f"Excel file not found: {config.EXCEL_FILE}")
                print(f"❌ Không tìm thấy file: {config.EXCEL_FILE}")
                return []
            
            workbook = load_workbook(config.EXCEL_FILE)
            worksheet = workbook.active
            
            keywords = []
            col = ord(config.EXCEL_COLUMN.upper()) - ord('A') + 1
            
            for row in worksheet.iter_rows(min_col=col, max_col=col):
                cell_value = row[0].value
                if cell_value and str(cell_value).strip():
                    keywords.append(str(cell_value).strip())
            
            logger.info(f"Read {len(keywords)} keywords from Excel")
            print(f"✅ Đã đọc {len(keywords)} từ khóa từ Excel")
            return keywords
            
        except Exception as e:
            logger.error(f"Error reading Excel: {e}")
            print(f"❌ Lỗi đọc Excel: {e}")
            return []
    
    def search(self, keyword):
        """Thực hiện tìm kiếm"""
        try:
            print(f"\n🔍 Tìm kiếm: {keyword}")
            logger.info(f"Searching: {keyword}")
            
            # Wait for search input
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, config.SEARCH_INPUT_SELECTOR))
            )
            
            # Type keyword with human-like speed
            self.human_like_typing(search_input, keyword)
            self.random_delay(1, 3)  # Delay trước khi click button
            
            # Click search button
            search_btn = self.driver.find_element(By.CSS_SELECTOR, config.SEARCH_BUTTON_SELECTOR)
            search_btn.click()
            logger.info(f"Clicked search button for: {keyword}")
            
            # Wait for results
            time.sleep(2)
            
            # Get results
            try:
                results = self.driver.find_elements(By.CSS_SELECTOR, config.RESULT_ITEM_SELECTOR)
                print(f"✅ Tìm thấy {len(results)} kết quả")
                logger.info(f"Found {len(results)} results")
                
                return results
            except:
                print("⚠️ Không tìm thấy kết quả")
                return []
                
        except Exception as e:
            logger.error(f"Search error: {e}")
            print(f"❌ Lỗi tìm kiếm: {e}")
            return []
    
    def click_result(self, result_element):
        """Click vào một kết quả"""
        try:
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView(true);", result_element)
            time.sleep(1)
            
            # Click the result
            link = result_element.find_element(By.CSS_SELECTOR, config.RESULT_LINK_SELECTOR)
            link.click()
            
            logger.info("Clicked on result")
            print("👆 Đã click vào kết quả")
            
            # Random viewing time
            view_time = random.uniform(config.MIN_VIEW_TIME, config.MAX_VIEW_TIME)
            print(f"📖 Xem {view_time:.0f} giây...")
            
            # Scroll while viewing
            if config.RANDOM_SCROLL:
                time.sleep(view_time / 2)
                self.random_scroll()
                time.sleep(view_time / 2)
            else:
                time.sleep(view_time)
            
            logger.info(f"Viewed for {view_time:.2f} seconds")
            
            # Go back
            self.driver.back()
            time.sleep(2)
            
            return True
            
        except Exception as e:
            logger.error(f"Click error: {e}")
            print(f"❌ Lỗi click: {e}")
            return False
    
    def run_automation(self):
        """Chạy automation chính"""
        try:
            # Đọc từ khóa
            keywords = self.read_keywords_from_excel()
            if not keywords:
                print("❌ Không có từ khóa để test")
                return
            
            # Mở website
            print(f"\n🌐 Mở website: {config.TARGET_WEBSITE}")
            self.driver.get(config.TARGET_WEBSITE)
            self.random_delay(2, 4)
            
            # Loop qua từng từ khóa
            for idx, keyword in enumerate(keywords, 1):
                print(f"\n{'='*50}")
                print(f"📍 Từ khóa {idx}/{len(keywords)}")
                print(f"{'='*50}")
                
                # Tìm kiếm
                results = self.search(keyword)
                
                if results and config.CLICK_RANDOM_LINKS:
                    # Click vào 1-3 kết quả ngẫu nhiên
                    num_clicks = random.randint(1, min(3, len(results)))
                    selected_results = random.sample(results, num_clicks)
                    
                    for click_idx, result in enumerate(selected_results, 1):
                        print(f"\n  Link {click_idx}/{num_clicks}")
                        self.click_result(result)
                        
                        # Delay trước search tiếp theo
                        if click_idx < num_clicks:
                            self.random_delay()
                
                # Delay trước từ khóa tiếp theo
                if idx < len(keywords):
                    self.random_delay()
                
                # Refresh page
                self.driver.refresh()
                self.random_delay(1, 2)
            
            print("\n✅ Automation hoàn thành!")
            logger.info("Automation completed successfully")
            
        except Exception as e:
            logger.error(f"Automation error: {e}")
            print(f"❌ Lỗi: {e}")
        
        finally:
            self.driver.quit()
            print("Browser đóng")

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          TEST AUTOMATION TOOL - Demo Version              ║
    ║                 v1.0.0                                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print("📋 Kiểm tra cấu hình...")
    print(f"  ├─ Target website: {config.TARGET_WEBSITE}")
    print(f"  ├─ Excel file: {config.EXCEL_FILE}")
    print(f"  ├─ Delay: {config.MIN_DELAY}-{config.MAX_DELAY}s")
    print(f"  └─ View time: {config.MIN_VIEW_TIME}-{config.MAX_VIEW_TIME}s")
    
    input("\n⏱️  Nhấn Enter để bắt đầu automation... (hoặc Ctrl+C để hủy)")
    
    automation = TestAutomation()
    automation.run_automation()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Đã hủy bởi người dùng")
        sys.exit(0)

"""
Configuration file for Test Automation Tool
Tùy chỉnh các settings tại đây
"""

# Website cần test
TARGET_WEBSITE = "file://" + r"C:\path\to\website\index.html"  # Thay đường dẫn tại đây

# Tên file Excel chứa từ khóa
EXCEL_FILE = "keywords.xlsx"
EXCEL_COLUMN = "A"  # Cột chứa từ khóa (A, B, C, v.v.)

# Output file
OUTPUT_CSV = "results.csv"

# Delays (giây)
MIN_DELAY = 120  # 2 phút
MAX_DELAY = 300  # 5 phút

# Viewing time (giây)
MIN_VIEW_TIME = 120  # 2 phút
MAX_VIEW_TIME = 600  # 10 phút

# Browser settings
HEADLESS = False  # Set True để ẩn browser
BROWSER_WINDOW_SIZE = (1920, 1080)

# Selectors (CSS/XPath) - Thay đổi theo website của bạn
SEARCH_INPUT_SELECTOR = "#searchInput"
SEARCH_BUTTON_SELECTOR = "#searchBtn"
RESULT_ITEM_SELECTOR = ".result-item"
RESULT_LINK_SELECTOR = ".result-link"

# Search actions
RANDOM_SCROLL = True  # Tự động scroll khi xem kết quả
CLICK_RANDOM_LINKS = True  # Click vào các link ngẫu nhiên

# Logging
LOG_ACTIONS = True
LOG_FILE = "automation.log"

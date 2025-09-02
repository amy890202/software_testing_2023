from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 設定 ChromeOptions
service = Service("/usr/bin/chromedriver")
options = Options()
options.add_argument("--headless")  
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)

# 開啟 NYCU 首頁
driver.get("https://www.nycu.edu.tw/")

# Debug：印出前 1000 個字，方便在 CI log 檢查 DOM
print("=== DEBUG: page_source start ===")
print(driver.page_source[:1000])
print("=== DEBUG: page_source end ===")

# 等待 <body> 載入
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

# 嘗試找到第二個 menu link
try:
    el = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "nav ul li:nth-child(2) a"))
    )
    el.click()
except Exception as e:
    print("⚠️ Menu element not found:", e)
    driver.quit()
    exit(1)

# 等待第一篇文章的 su-post 出現並點擊
try:
    a = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "su-post"))
    )
    b = a.find_element(By.CSS_SELECTOR, ".su-post > a")
    b.click()
except Exception as e:
    print("⚠️ Article element not found:", e)
    driver.quit()
    exit(1)

# 抓取文章標題
title = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "single-post-title"))
)
print("文章標題:", title.text)

# 抓取文章段落
content = driver.find_elements(By.TAG_NAME, "p")
for i in content:
    print(i.text)

# 開新分頁 → Google 搜尋
driver.switch_to.new_window("tab")
driver.get("https://www.google.com")

search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "q"))
)
search_box.send_keys("311581024")
search_box.send_keys(Keys.RETURN)

# 取得搜尋結果
result_element = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "DKV0Md"))
)

if len(result_element) >= 2:
    print("搜尋結果:", result_element[1].text)
else:
    print("There are no search results.")

driver.quit()

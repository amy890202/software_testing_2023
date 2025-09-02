from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--window-size=1920,1080')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


service = Service("/usr/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # CI 環境必須 headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.nycu.edu.tw/")
driver.maximize_window()

driver.implicitly_wait(50)
el = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/section[2]/div/div/div[1]/div/div/div/div/nav[1]/ul/li[2]/a")
el.click()

driver.implicitly_wait(50)
a = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME,"su-post"))
b= a.find_element(By.CSS_SELECTOR,".su-post > a")
b.click()

driver.implicitly_wait(50)
title = driver.find_element(By.CLASS_NAME,"single-post-title")
print(title.text)#get_attribute("innerHTML")
driver.implicitly_wait(50)
content = driver.find_elements(By.TAG_NAME, 'p')
for i in content:
    print(i.text)

driver.switch_to.new_window('tab')
driver.get("https://www.google.com")
driver.implicitly_wait(50)

search_box = driver.find_element(By.NAME,"q")
search_box.send_keys("311581024")
search_box.send_keys(Keys.RETURN)

driver.implicitly_wait(50)
result_element = driver.find_elements(By.CLASS_NAME, "DKV0Md")#By.TAG_NAME, 'h3'
driver.implicitly_wait(50)
if len(result_element) >= 2:
    print(result_element[1].text)
else:
    print("There are no search results.")

driver.quit()

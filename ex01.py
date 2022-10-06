from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
browser = webdriver.Chrome(executable_path="/home/ubuntu/proj/chrome/chromedriver", options=chromeOptions)
browser.get("http://www.baidu.com")
print("Title: %s" % browser.title)
browser.quit()
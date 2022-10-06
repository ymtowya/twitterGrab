from os import name
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
from trend import Trend
from trendStore import TrendStore
import re

CSV_FILE_PATH_PATTERN = "./result/result{date}.csv"
CSV_HEADER = ['Time',
              'No.',
              'Content',
              'Hotness']
CSV_BLANK_ROW = ['', '', '', '']
# /html/body/div[1]/div[2]/div/div[2]/div[1]/table/tbody/tr[4]/td[2]/a
ROOT_XPATH = "/html/body/div[1]/div[2]/div/div[2]/div[1]/table/tbody"
# "/usr/local/bin/chromedriver"
# "/home/ubuntu/proj/chrome/chromedriver"
# "/usr/bin/chromedriver"
# "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
CHROME_DRIVER_PATH = "/home/ubuntu/proj/chrome/chromedriver"
CHROME_SERVICE = Service(CHROME_DRIVER_PATH)
SLEEP_SECS = 60
LOCAL_TIME = time.localtime()

myConfig = {}
myConfig['dbname'] = "weibotrends"
myConfig['date'] = time.strftime("%Y%m%d", LOCAL_TIME)
myConfig['host'] = "localhost"
myConfig['port'] = 3307
myConfig['user'] = "towya"
myConfig['password'] = "123456"

class weiboHotLineSpider:
    def __init__(self, browser, store):
        self.browser = browser
        self.csvRows = []
        self.hotlines = []
        self.nowStamp = ""
        self.dateStamp = ""
        self.timeStamp = 0
        self.csvName = "test.csv"
        self.trends = []
        self.store = store
        return

    def writeCSV(self):
        #print(f'--开始写入{CSV_FILE_PATH}文件的操作--')
        with open(self.csvName,'a+', encoding='UTF-8')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(CSV_BLANK_ROW)
            f_csv.writerow(CSV_HEADER)
            f_csv.writerows(self.csvRows)
        print(f'++已完成写入{self.csvName}文件的操作++')
    
    def getContent(self):
        pass
        try:
            self.nowStamp = time.strftime("%Y-%m-%d %H:%M:%S", LOCAL_TIME)
            self.dateStamp = time.strftime("%Y%m%d", LOCAL_TIME)
            self.timeStamp = int(time.strftime("%H%M", LOCAL_TIME))
            self.csvName = CSV_FILE_PATH_PATTERN.format(date = self.dateStamp)
            driver = self.browser            
            driver.get('https://s.weibo.com/top/summary/')
            print("\nWork Log at " + self.nowStamp + " .\n")
            print("Get Already!") # Let the user actually see something!
            time.sleep(SLEEP_SECS)
            self.hotlines = driver.find_elements(By.XPATH, ROOT_XPATH)
        except NoSuchElementException:
            print("Error Log: \n" + time.strftime("%Y-%m-%d %H:%M:%S", LOCAL_TIME) + " Failed to fetch data.\n\n")
            pass

    def dealContent(self):
        pass
        try:
            if len(self.hotlines) > 0:
                self.csvRows = []
                self.trends = []
                self.csvRows.append([self.nowStamp, '', '', ''])
                try:
                    #hotpots = self.hotlines[0].find_elements_by_tag_name("tr")
                    hotpots = self.hotlines[0].find_elements(By.TAG_NAME, "tr")
                    print(len(hotpots))
                    for hotpot in hotpots:
                        hottds = hotpot.find_elements(By.TAG_NAME, "td")
                        if len(hottds) >= 2:
                            tmpRow = []
                            tmpRow.append('') # tmpRow.append(nowStamp)
                            tmpRow.append(hottds[0].text) # 1
                            hottext = hottds[1].find_element(By.TAG_NAME, "a")
                            tmpRow.append(hottext.text) # 2
                            try:
                                hotness = hottds[1].find_element(By.TAG_NAME, "span")
                                tmpRow.append(hotness.text) # 3
                            except NoSuchElementException:
                                tmpRow.append(' ')
                            finally:
                                pass
                            
                            if hottds[0].text.isdigit():
                                myTrend = Trend(int(hottds[0].text), hottext.text, hotness.text)
                                self.trends.append(myTrend)
                            self.csvRows.append(tmpRow)
                except NoSuchElementException:
                    pass
                finally:
                    self.writeCSV()
                    pass
            else:
                print("Error Log 0: \n" + time.strftime("%Y-%m-%d %H:%M:%S", LOCAL_TIME) + " Failed to fetch data.\n\n")
        except NoSuchElementException:
            print('报错：NoSuchElementException')
    
    def storeContent(self):
        try:
            if not self.store.checkTable():
                self.store.createAndLog()
            if self.store.insertTrends(self.trends, self.timeStamp):
                print("INSERT SUCCESS INTO DBs")
        finally:
            pass

    def run(self):
        try:
            self.getContent()
            self.dealContent()
            self.storeContent()
        finally:
            pass

# driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

# driver.quit()

if __name__ == "__main__":

    try:

        chromeOptions = webdriver.ChromeOptions() 
        chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
        chromeOptions.add_argument("--no-sandbox") 
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument("--disable-setuid-sandbox") 

        chromeOptions.add_argument("--remote-debugging-port=9222")  # this

        chromeOptions.add_argument("--disable-dev-shm-using") 
        chromeOptions.add_argument("--disable-extensions") 
        chromeOptions.add_argument("--disable-gpu") 
        chromeOptions.add_argument("start-maximized") 
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.headless = True
        # chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 

        browser = webdriver.Chrome(service=CHROME_SERVICE, options=chromeOptions)
        myStore = TrendStore(myConfig)
        mySpider = weiboHotLineSpider(browser, myStore)
        mySpider.run()
        browser.delete_all_cookies()
    except NoSuchElementException:
        pass
    finally:
        browser.quit()

# //*[@id="pl_top_realtimehot"]/table/tbody/tr[2]/td[2]/a
# /html/body/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/a
# /html/body/div[1]/div[2]/div[2]/table/tbody/tr[3]/td[2]/a
# /html/body/div[1]/div[2]/div[2]/table/tbody/tr[1]

# search_box.send_keys('ChromeDriver')

# search_box.submit()

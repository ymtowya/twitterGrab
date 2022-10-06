from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv

CSV_FILE_PATH = "test20211110.csv"
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
CHROME_DRIVER_PATH = "/home/ubuntu/proj/chrome/chromedriver"
SLEEP_SECS = 64

class weiboHotLineSpider:
    def __init__(self, browser):
        self.browser = browser
        self.csvRows = []
        self.hotlines = []
        self.nowStamp = ''
        return

    def writeCSV(self):
        #print(f'--开始写入{CSV_FILE_PATH}文件的操作--')
        with open(CSV_FILE_PATH,'a+')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(CSV_BLANK_ROW)
            f_csv.writerow(CSV_HEADER)
            f_csv.writerows(self.csvRows)
        print(f'++已完成写入{CSV_FILE_PATH}文件的操作++')
    
    def getContent(self):
        pass
        try:
            self.nowStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            driver = self.browser
            print("\nWork Log at " + self.nowStamp + " .\n")
            driver.get('https://s.weibo.com/top/summary/')
            print("Get Already!") # Let the user actually see something!
            time.sleep(SLEEP_SECS)
            self.hotlines = driver.find_elements_by_xpath(ROOT_XPATH)
            # time.sleep(1)
            # print("Elements Find Already!")
        except NoSuchElementException:
            print("Error Log: \n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Failed to fetch data.\n\n")
            pass

    def dealContent(self):
        pass
        try:
            if len(self.hotlines) > 0:
                self.csvRows = []
                self.csvRows.append([self.nowStamp, '', '', ''])
                try:
                    hotpots = self.hotlines[0].find_elements_by_tag_name("tr")
                    print(len(hotpots))
                    for hotpot in hotpots:
                        hottds = hotpot.find_elements_by_tag_name("td")
                        if len(hottds) >= 2:
                            tmpRow = []
                            tmpRow.append('') # tmpRow.append(nowStamp)
                            tmpRow.append(hottds[0].text)
                            hottext = hottds[1].find_element_by_tag_name("a")
                            tmpRow.append(hottext.text)
                            try:
                                hotness = hottds[1].find_element_by_tag_name("span")
                                tmpRow.append(hotness.text)
                            except NoSuchElementException:
                                tmpRow.append(' ')
                            finally:
                                pass

                            self.csvRows.append(tmpRow)
                except NoSuchElementException:
                    pass
                finally:
                    self.writeCSV()
            else:
                print("Error Log 0: \n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Failed to fetch data.\n\n")
        except NoSuchElementException:
            print('报错：NoSuchElementException')
    
    def run(self):
        try:
            self.getContent()
            self.dealContent()
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

        browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chromeOptions)
        mySpider = weiboHotLineSpider(browser)
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

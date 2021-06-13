import re
import sys
import os
from os import system
from selenium import webdriver
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
options.headless = True


system("title Yad2Jumper")

driver = webdriver.Chrome('chromedriver', options=options)
driver.set_window_position(-10000,0)

driver.get("https://my.yad2.co.il/login.php")

if ("loginForm" in driver.page_source):
    print("Stating login process")
    elem = driver.find_element_by_name("UserName")
    elem.clear()
    elem.send_keys("EMAIL@gmail.com")
    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys("Password")
    driver.find_element_by_id('submitLogonForm').click()
    print("Login Success")

if ("row errors" in driver.page_source):
    print("Wrong ID/Password")

if ("personalInformation" in driver.page_source):
    for ID in range(10):
        print("Looking for ADs at CatID=" + str(ID))
        driver.get("https://my.yad2.co.il/newOrder/index.php?action=personalAreaFeed&CatID="+ str(ID) + "&SubCatID=0")
        arry = [int(s) for s in re.findall(r'\b\d+\b', driver.page_source)]
        y = list(set(arry))
        for x in y:
            if (x > 30000000) and (x < 69999999):  # OrderID range
                print("AD Found: " + str(x))
                driver.get(
                    "https://my.yad2.co.il/newOrder/index.php?action=personalAreaViewDetails&CatID="+ str(ID) +"&SubCatID=0&OrderID=" + str(
                        x))
                if ("bounceRatingOrderBtn" in driver.page_source):
                    driver.find_element_by_id('bounceRatingOrderBtn').click()
                    print("AD been Promoted!")
                    driver.get(
                        "https://my.yad2.co.il/ExpiredMsg/index.php?Username=dnJ0azUwQGdtYWlsLmNvbQ==&utm_source=AdExpired&utm_medium=email&utm_campaign=AdExpired&utm_content=Secondhand&oid=" + str(
                            x))
                    driver.get("https://my.yad2.co.il/ExpiredMsg/index.php?auid=VXNlcm5hbWU9dnJ0azUwQGdtYWlsLmNvbSZvaWQ9NDM1MjI3MzQ%3D")
                else:
                    print("Fail to Promote AD")


driver.close()

os.system('taskkill /F /IM chromedriver.exe')
quit()
sys.exit()
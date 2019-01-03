from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

#Login credentials
username = "username"
password = "password"

#totalAirports = 3 #actual total is 482 as of 12/24/18

driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
#driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get('https://someurl.com/')
driver.find_element_by_name('username').send_keys('{}'.format(username))
driver.find_element_by_name('userpassword').send_keys('{}'.format(password))
driver.find_element_by_name('Login').click()

#After successful login, takes to the airport search page, where: 

#TODO: Loop it for all airports

#accesing the airport code from the dropdown
driver.find_element_by_xpath('//li[@data-option-array-index="314"]').click()
driver.find_element_by_xpath('//button[@class="btn btn-success"]').click()
time.sleep(2)

#Extracting table of Contacts
driver.find_element_by_xpath('//ul[@id="myTabs"]/li/a[@href="#profile"]').click()
time.sleep(2)
driver.find_element_by_xpath('//select[@name="table-view-Data_length"]/option[@value="25"]').click()
time.sleep(1)
table = driver.find_element_by_xpath('//div[@id="table-view-Data_wrapper"]/table[@id="table-view-Data"]')
table_html = table.get_attribute('outerHTML')

df = read_html(table_html)
print(df)

driver.close()

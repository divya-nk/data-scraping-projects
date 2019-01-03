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

#looping it through all Airports

for i in range(1, totalAirports+1):
    
    select = Select(driver.find_element_by_xpath('//select[@name="c_aid"]'))
    driver.find_element_by_css_selector(".chosen-container.chosen-container-single").click()
    time.sleep(2)

    #accesing the airport code from the dropdown
    driver.find_element_by_xpath('//li[@data-option-array-index="{}"]'.format(i)).click()
    driver.find_element_by_xpath('//button[@class="btn btn-success"]').click()
    time.sleep(2)

    if driver.find_element_by_xpath('//div[@class="alert alert-danger alert-dismissible"]'):
        print(driver.find_element_by_xpath('//div[@class="alert alert-danger alert-dismissible"]').text)
    
    else:

        #capture all tables on the page
        tables = driver.find_elements_by_xpath("//div[@class='panel panel-primary']//table")

        for table in tables:
            if table.get_attribute('id') == 'example':
                table.find_element_by_xpath('../div[@class="dataTables_length"]//select[@name="example_length"]/option[@value="-1"]').click()
                time.sleep(1)
            table_html = table.get_attribute('outerHTML')
            df = read_html(table_html)
            print(df)

#TODO: export data to xcel/sql server?
    
#Log out and close the browser    
driver.find_element_by_xpath('//input[@value="Log out"]').click()
time.sleep(2)
driver.close()

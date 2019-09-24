from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from IPython.display import display_html



t1 = time.time()
url = 'https://hosting.portseattle.org/contractsweb/ConSummaryPage.aspx'
driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe')
wait = WebDriverWait(driver, 10)
driver.get(url)
master_table = pd.DataFrame()
vendor_table = pd.DataFrame()
amdt_details = pd.DataFrame()

for j in range(32,46):
    time.sleep(3)
    #if z ==1:
    #    if driver.find_elements_by_link_text(str('...')): 
    #        driver.find_elements_by_link_text(str('...'))[0].click()
    #    if driver.find_elements_by_link_text(str('...')): 
    #        driver.find_elements_by_link_text(str('...'))[1].click()
    #z=5
    
    tables = driver.find_elements_by_xpath("//div//table[@id = 'oGridView']")
    
    for table in tables:
        table_html = table.get_attribute('outerHTML')
        df = pd.read_html(table_html)
        df = df[0].iloc[1:26,0:4]
        master_table = master_table.append(df)
        for i in range(len(df)):
            driver.find_element_by_xpath("//div//table[@id = 'oGridView']//a[@href ='ConDetailsPage.aspx?id="+df.iloc[i,1]+"']").click()
            #driver.find_element_by_link_text(df.iloc[i,0]).click()
            time.sleep(2)
            tables = driver.find_elements_by_xpath("//div//table[@id = 'DetailsView1']")
            for table in tables:
                table_html = table.get_attribute('outerHTML')
                vt = pd.read_html(table_html)
                vt = vt[0].T.iloc[1:,:]
                vendor_table = vendor_table.append(vt)
            if driver.find_elements_by_xpath("//div//table[@id = 'GridView']"):
                amendments = driver.find_elements_by_xpath("//div//table[@id = 'GridView']")
                for amd in amendments:
                    amd_html = amd.get_attribute('outerHTML')
                    amdt = pd.read_html(amd_html)
                    amdt = amdt[0].iloc[1:, :]
                    amdt['Vendor Name'] = df.iloc[i,0]
                    amdt['Contract ID'] = df.iloc[i,1]
                    amdt_details = amdt_details.append(amdt)
            #driver.navigate().back()
            driver.execute_script("window.history.go(-1)")
            time.sleep(2)
    driver.find_element_by_link_text(str(j)).click()

master_table.reset_index(inplace = True)
master_table.drop(columns = ['index'], inplace = True)
master_table.rename(columns = {0: "Vendor Name", 1: "Contract ID", 2: "Title/Purpose", 3: "Execution Date"}, inplace = True)
vendor_table.reset_index(inplace = True)
vendor_table.drop(columns = ['index'], inplace = True)
vendor_table.rename(columns = {0: 'Vendor Name' , 1:'Contract ID', 2: 'Title/Purpose' , \
                               3:'Execution Date' , 4: 'Original Expiration Date' , 5: 'Current Expiration Date' , \
                               6: 'Original Contract Amount', 7: 'Current Contract Amount' , 8: 'Selection Process' , \
                               9: 'Funding Sources' , 10: 'Modifications'}, inplace = True)

amdt_details.reset_index(inplace = True)
amdt_details.drop(columns = ['index'], inplace = True)
amdt_details.rename(columns = {0:'Mod #', 1:'Execution Date', 2: 'Description', 3:'Change Type', \
                               4: 'Budget Change', 5: 'Expiration Date Change'}, inplace = True)
t2 = time.time()
print('Total time taken to loop through 45 pages: {} minutes '.format((t2-t1)/60))

master_table.to_csv('master_table2.csv')
vendor_table.to_csv('vendor_table2.csv')
amdt_details.to_csv('amdt_details2.csv')

import time
from selenium import webdriver

driver = webdriver.Chrome('C:\\Users\\mo.battah\\Downloads\\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://login.akken.com')
companyID = driver.find_element_by_name("companyuser")
companyID.send_keys("company")
username = driver.find_element_by_name("username")
username.send_keys("user")
password = driver.find_element_by_name('pass')
password.send_keys("pass")
login = driver.find_element_by_name('submit')
login.submit()
time.sleep(5)
driver.get('https://appserver.akken.com/BSOS/Marketing/Candidates/Candidates.php');
time.sleep(5)
checkbox = driver.find_element_by_xpath('//*[@id="tag48.top.item:0/box"]/label/span')
checkbox.click()
exportbutton = driver.find_element_by_xpath('//*[@id="toplink"]/tr/td[3]/div/ul/li/a')
exportbutton.click()
time.sleep(1)
exportybutton = driver.find_element_by_xpath('//*[@id="toplink"]/tr/td[3]/div/ul/li/ul/li[2]/a')
exportybutton.click()
time.sleep(3)
#savebutton = driver.find_element_by_xpath('//*[@id="main"]/div/table/tbody/tr[5]/td/div/a')
#savebutton = driver.find_element_by_xpath('//*[@id="main"]/div/table/tbody/tr[5]/td/div/a/i')
#savebutton.click()
script1 = "<a href=\"javascript:void(0);\" onclick=\"DoCrmExport('Candidates');\" class=\"akkenPopupBtn\"><i class=\"fa fa-thumbs-up\"></i>Save</a>"
try: driver.execute_script(script1)
except SyntaxError:
    print("Oh well doesnt matter")
script2 = 'DoCrmExport(\'Candidates\');'

driver.execute_script(script2)
time.sleep(10)


time.sleep(10) 
driver.quit()

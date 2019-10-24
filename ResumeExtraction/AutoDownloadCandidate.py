import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\\Users\\mo.battah\\Downloads\\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://login.akken.com')
companyID = driver.find_element_by_name("companyuser")
companyID.send_keys("companyname")
username = driver.find_element_by_name("username")
username.send_keys("user")
password = driver.find_element_by_name('pass')
password.send_keys("password")
login = driver.find_element_by_name('submit')
login.submit()
time.sleep(5)
driver.get('https://appserver.akken.com/BSOS/Marketing/Candidates/Candidates.php');
time.sleep(5)
driver.find_element_by_xpath('//*[@id="show_recs"]/option[4]').click()
for x in range(0,80):
    time.sleep(7)
    checkbox = driver.find_element_by_xpath('//*[@id="chk"]')
    checkbox.send_keys(" ")
    exportbutton = driver.find_element_by_xpath('//*[@id="toplink"]/tr/td[3]/div/ul/li/a')
    exportbutton.click()
    time.sleep(1)
    exportybutton = driver.find_element_by_xpath('//*[@id="toplink"]/tr/td[3]/div/ul/li/ul/li[2]/a')
    exportybutton.click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="mainbody"]/table/tbody/tr[1]/td[3]/table/tbody/tr[6]/td/table/tbody/tr/td[3]/div/table/tbody/tr/td[4]/a').send_keys(Keys.RETURN)

driver.quit()







#may be helpful
#driver.find_element_by_xpath("//div[@id='mainbody']/table/tbody/tr/td[3]/table/tbody/tr[6]/td/table/tbody/tr/td[3]/div/table/tbody/tr/td[4]/a/i").click()
#driver.find_element_by_xpath("//div[@id='tag48.top.item:0/box']/label/span").click()
# #####################
# # savebutton = driver.find_elements_by_xpath('//*[@id="main"]/div/table/tbody/tr[5]/td/div/a')
# # print(savebutton)
# #savebutton = driver.find_element_by_xpath('//*[@id="main"]/div/table/tbody/tr[5]/td/div/a/i')
# #savebutton.click()
# script1 = '<a href="javascript:void(0);" onclick="DoCrmExport(\'Candidates\');" class="akkenPopupBtn"><i class="fa fa-thumbs-up"></i>Save</a>'
# # print(script1)
# # script1 = script1.replace('\\','')
# # print(script1)
# # try: driver.execute_script(script1)
# # except:
# #     print("Oh well doesnt matter")
# # script2 = 'DoCrmExport("Candidates");'
# #
# # driver.execute_script(script2)





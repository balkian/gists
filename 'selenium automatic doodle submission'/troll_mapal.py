from selenium import webdriver
from selenium.webdriver.support.ui import Select
from faker import Factory
import random
fake = Factory.create('it_IT')

dood = "http://doodle.com/arcgntcrzqeqr2c6"
driver = webdriver.Firefox()
driver.implicitly_wait(3) # seconds

for i in range(0,10):
    name = fake.first_name()
    driver.get(dood)
    nam = driver.find_element_by_xpath('//*[@id="pname"]')
    nam.send_keys(name)
    print nam
    option = random.randint(0,2)
    opt = driver.find_element_by_xpath('//*[@id="option{}"]'.format(option))
    opt.click()
    sav = driver.find_element_by_xpath('//*[@id="save"]')
    sav.click()
    import time
    time.sleep(2)

driver.quit()

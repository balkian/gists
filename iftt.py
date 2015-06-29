from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

home = 'https://ifttt.com/recipes';
driver = webdriver.Firefox()
#driver.set_window_size(1024, 768)

driver.get(home)

wait = WebDriverWait(driver, 10)

for i in xrange(50):
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'load_more_btn')))
    element.click()

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#import selenium.webdriver.firefox.webdriver as fwb
import selenium.webdriver.chrome as cwd
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import csv
from urllib import request
from urllib.error import HTTPError

home = 'https://www.aliexpress.com/';

ATTRS = ['time', 'id', 'image', 'store', 'status', 'title', 'price', 'quantity']


# ff_bin = fwb.FirefoxBinary(firefox_path='/usr/bin/firefox')
# ff_profile = fwb.FirefoxProfile()
options = cwd.options.Options()
options.binary_location = '/usr/bin/chromium'
options.add_argument('--lang=en')
options.add_argument('--user-data-dir=/tmp/aliexpress')
driver = webdriver.Chrome(chrome_options=options)
# driver.set_window_size(1024, 768)

def login():
    # Login
    driver.get(home)
    try:
        lb = driver.find_element_by_link_text('Go to Global Site (English)')
        lb.click()
    except:
        print('Already in English')
        pass
    wait = WebDriverWait(driver, 10)
    login = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Sign in')))
    login.click()
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'account-name')))
    except Exception as ex:
        print('My orders not found')
        print(ex)
        driver.quit()
        exit()

def gotoorders():
    wait = WebDriverWait(driver, 10)
    element = driver.find_element_by_class_name('account-name')
    element.click()
    orders = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'My Orders')))
    orders.click()
    orders = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'My Orders')))

def scrape_orders_page():
    ordertable = driver.find_element_by_id('buyer-ordertable')
    for order in ordertable.find_elements_by_tag_name('tbody'):
        # head = element.find_element_by_class_name('order-head')
        # body = element.find_element_by_class_name('order-body')
        title = order.find_element_by_class_name('product-title').text
        status = order.find_element_by_class_name('order-status').text
        time = order.find_element_by_xpath(".//span[text()[contains(.,'Order time')]]/following-sibling::span[1]").text
        orderid = order.find_element_by_xpath(".//span[text()[contains(.,'Order ID')]]/following-sibling::span[1]").text
        store = order.find_element_by_xpath(".//span[text()[contains(.,'Store name')]]/following-sibling::span[1]").text
        for product in order.find_elements_by_class_name('product-sets'):
            pamount = product.find_element_by_class_name('product-amount').find_elements_by_tag_name('span')
            price, quantity = (elem.text for elem in pamount[:2])
            image = product.find_element_by_xpath(".//div[@class='product-left']/a/img").get_attribute('src').rsplit('_', 1)[0]

            imagefile = image.split('/')[-1]
            if not os.path.exists(imagefile):
                try:
                    request.urlretrieve(image, imagefile)
                except HTTPError:
                    print('Couldn\'t downloaded image:', image)
            yield {'time': time,
                'id': orderid,
                'image': image,
                'store': store,
                'status': status,
                'title': title,
                'price': price,
                'quantity': quantity}


def orders():
    gotoorders()
    yield driver
    yield from next_orders_page()

def next_orders_page():
    lb = driver.find_element_by_link_text('Next')
    lb.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyer-ordertable')))
    yield driver
    yield from next_orders_page()

login()
from itertools import islice
with open('list.csv', 'w') as f:
    fw = csv.DictWriter(f, ATTRS)
    fw.writeheader()
    for i in islice(orders(), None):
        for element in scrape_orders_page():
            fw.writerow(element)
# driver.save_screenshot('screen.png')

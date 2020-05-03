from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get("https://www.realtor.com/realestateandhomes-search/Minneapolis_MN/pg-1")

time.sleep(2)
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

l1 = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
for link in soup.find_all('a'):
    if link.get('href') is not None and "realestateandhomes-detail" in link.get('href'):
        if link.get('href') not in l1:
            l1.append(link.get('href'))

driver.get("https://www.realtor.com/realestateandhomes-search/Minneapolis_MN/pg-2")


time.sleep(2)
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, 'html.parser')
for link in soup.find_all('a'):
    if link.get('href') is not None and "realestateandhomes-detail" in link.get('href'):
        if link.get('href') not in l1:
            l1.append(link.get('href'))
# driver.quit()

print (len(l1))
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, csv, json
from bs4 import BeautifulSoup
from tqdm import tqdm

driver = webdriver.Chrome()
url = "https://webcache.googleusercontent.com/search?q=cache:1QWyjnW3Y0EJ:https://www.zillow.com/homedetails/1802-Willowwood-Cir-Harker-Heights-TX-76548/49515512_zpid/+&cd=2&hl=en&ct=clnk&gl=us"
driver.get(url)

# time.sleep(10)

# print (driver.page_source)

soup = BeautifulSoup(driver.page_source, 'html.parser')
for link in soup.find_all("script", id="hdpApolloPreloadedData"):
    data = (link.text)

data = json.loads(data)
data1 = json.loads(data['apiCache'])

for x in data1.keys():
    if 'VariantQuery' in x:
        print (x)
        main = x
    else:
        other_main = x

data1 = json.loads(data['apiCache'])[main]["property"]

with open('data.json', 'w') as outfile:
    json.dump(data1, outfile)

data2 = json.loads(data['apiCache'])[other_main]["property"]

with open('data1.json', 'w') as outfile:
    json.dump(data2, outfile)

# driver.quit()
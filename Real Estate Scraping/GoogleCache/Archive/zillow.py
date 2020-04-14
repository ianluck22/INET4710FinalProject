from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, csv, json
from bs4 import BeautifulSoup
from tqdm import tqdm

def getInformation(urls):
    driver = webdriver.Chrome()
    results = []
    for url in tqdm(urls):
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.find_all("script", id="hdpApolloPreloadedData"):
            data = (link.text)

        data = json.loads(data)
        data1 = json.loads(data['apiCache'])

        for x in data1.keys():
            if 'VariantQuery' in x:
                main = x
            else:
                other_main = x

        data1 = json.loads(data['apiCache'])[main]["property"]

        data2 = json.loads(data['apiCache'])[other_main]["property"]

        description = data2['description']
        taxAssessedValue = data2['taxAssessedValue']

        averageSchoolRating = 0
        for x in data2['schools']:
            averageSchoolRating += x['rating']
        averageSchoolRating/=len(data2['schools'])

        payload = data1
        payload['description'] = description
        payload['taxAssessedValue'] = taxAssessedValue
        payload['url'] = url
        results.append(payload)
    driver.quit()
    return results

urls = [
    "https://webcache.googleusercontent.com/search?q=cache:1QWyjnW3Y0EJ:https://www.zillow.com/homedetails/1802-Willowwood-Cir-Harker-Heights-TX-76548/49515512_zpid/+&cd=2&hl=en&ct=clnk&gl=us"
]

print(getInformation(urls)[0])
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, csv
from bs4 import BeautifulSoup
from tqdm import tqdm

def read_csv():
    list1 = []
    file = '../../propertyTrans.csv'
    with open(file) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            list1.append(row)
    return list1

driver = webdriver.Chrome()

with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = open("../../propertyTrans.csv", 'r').readline()[:-1].split(',')
    fieldnames.append("cacheLink")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in tqdm(read_csv()):
        count_retry = 0
        while True:
            try:
                count_retry += 1
                search_term = f"{row['addressLine1']} {row['stateOrProvince']} {row['zip']}"
                driver.get("http://www.google.com/search?q="+search_term.replace(' ', '%20'))
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                for link in soup.find_all('li'):
                    for a in link.find_all('a'):
                        if 'webcache' in a.get('href') and 'zillow' in a.get('href'):
                            driver.get(a.get('href'))
                            row['cacheLink'] = a.get("href")

                if 'cacheLink' not in row:
                    row['cacheLink'] = ""
                
                writer.writerow(row) 
                break
            except Exception as e:
                print ("Retrying because of", str(e))
                if count_retry < 3:
                    time.sleep(5)
                    continue
                else:
                    row['cacheLink'] = ""
                    writer.writerow(row) 
                    break
driver.close()

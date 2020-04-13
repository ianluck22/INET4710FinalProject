from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time, csv
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

FILE_NUMBER = 1

df = pd.read_feather(f"../../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft")
list_of_addresses = df[df["GoogleCacheLink"] == ""]["property"].to_list()

driver = webdriver.Chrome()

for address in tqdm(list_of_addresses):
    count_retry = 0
    while True:
        try:
            count_retry += 1
            search_term = f"{address}"
            driver.get("http://www.google.com/search?q="+search_term.replace(' ', '%20'))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cacheLink = ""
            for link in soup.find_all('li'):
                for a in link.find_all('a'):
                    if 'webcache' in a.get('href') and 'zillow' in a.get('href'):
                        driver.get(a.get('href'))
                        cacheLink = a.get("href")

            df.loc[df['property'] == address, ['GoogleCacheLink']] = cacheLink
            break

        except Exception as e:
            print ("Retrying because of", str(e))
            if count_retry < 3:
                time.sleep(5)
                continue
            else:
                cacheLink
                break

    df.to_feather(f"../../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft")

driver.close()

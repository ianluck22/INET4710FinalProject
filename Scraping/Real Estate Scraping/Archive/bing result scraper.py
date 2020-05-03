from bs4 import BeautifulSoup
import requests

def search(query):
    address = "http://www.bing.com/search?q=%s" % query
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    response = requests.get(address, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all("li", class_="b_algo"):
        for link1 in link.find_all("a"):
            if 'zillow' in link1.get('href'):
                #print (link1.get('href'))
                pass
        for x in link.find_all("div", class_="b_attribution"):
            print (x)


for x in range(1):
    search("311 Harvard St SE")


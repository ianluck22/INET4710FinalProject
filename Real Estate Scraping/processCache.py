import os, time, csv, json, rubberduck, sys, pickle, random
from bs4 import BeautifulSoup
from tqdm import tqdm


def getCacheResponse(url):
    response = rubberduck.search(url, bang='cache', no_redirect=0, skip_disambig=0)
    result = response.content
    return result


def getInformation(data):
    soup = BeautifulSoup(data, 'html.parser')
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
    if 'taxAssessedValue' not in data2:
        taxAssessedValue = -1
    else:
        taxAssessedValue = data2['taxAssessedValue']

    averageSchoolRating = 0
    for x in data2['schools']:
        averageSchoolRating += x['rating']
    averageSchoolRating/=len(data2['schools'])

    payload = data1
    payload["averageSchoolRating"] = averageSchoolRating
    payload['description'] = description
    payload['taxAssessedValue'] = taxAssessedValue

    return payload

FILE_NUMBER = sys.argv[1]
df = pickle.load(open(f"../datafiles/BingScraped/metroArea{FILE_NUMBER}.ft", "rb"))
list_of_urls = df[df["status"] == "NEW"]["ZillowURL"].to_list()

for url in tqdm(list_of_urls):
    content = getCacheResponse(url)
    try:
        payload = getInformation(content)
        del payload['listing_sub_type']
        for x in payload:
            try:
                df.loc[df['ZillowURL'] == url, [x]] = payload[x]
            except:
                pass
        df.loc[df['ZillowURL'] == url, ['status']] = "Completed"

    except Exception as e:
        df.loc[df['property'] == url, ['status']] = "NEW"
        print (str(e), content[:50])
    
    time.sleep(random.randint(5, 10))
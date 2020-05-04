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
        data = (link.contents[0])

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
df = pickle.load(open(f"../../datafiles/BingScraped/metroArea{FILE_NUMBER}.ft", "rb"))
list_of_urls = df[df["status"] == "NEW"]["ZillowURL"].to_list()

counter = 0
for url in tqdm(list_of_urls):
    counter += 1
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
        if "block" in str(content) and "CAPTCHA" in str(content) and "unusual traffic from your computer network" in str(content):
            df.loc[df['ZillowURL'] == url, ['status']] = "NEW"
            print ("Google Blocked Cache Hit")
        else:
            df.loc[df['ZillowURL'] == url, ['status']] = "Error"
            print ("Error Accessing")
    
    pickle.dump(df, open(f"../../datafiles/BingScraped/metroArea{FILE_NUMBER}.ft", "wb"))

    if counter != 0 and counter % 38 == 0:
        sleep_time = 60 * (60 + 15) + random.randint(5 * 60, 10 * 60)  # 1 h + 5 to 10 minutes
        time.sleep(sleep_time)
    # time.sleep(4)

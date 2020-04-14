import os, time, csv, json
from bs4 import BeautifulSoup
from tqdm import tqdm

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


subscription_key = "4a33e7fb450a4130b44255260eb264df"
assert subscription_key

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

import requests

def getURL(search_term):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    for x in (search_results['webPages']['value']):
        if 'zillow' in x['url']:
            return (x['url'])
    return None
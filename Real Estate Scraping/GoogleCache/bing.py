subscription_key = "dde20fdc381a4e3791d636e112c5d02f"
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
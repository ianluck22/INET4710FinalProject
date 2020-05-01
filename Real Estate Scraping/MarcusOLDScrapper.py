import json
from requests import Request, Session
from time import sleep
from urllib.parse import unquote


# Tried something with the ddg api which didn't work. Swap out for bing api
def get_zillow_url(address):
    payload = {
        'format': 'json',
        'no_redirect': 1,
        'q': '!bing ' + address
    }

    s = Session()
    req = Request('GET', 'https://api.duckduckgo.com', params=payload)
    prepped = s.prepare_request(req)
    prepped.url = prepped.url.replace('%21', '!')
    prepped.url = prepped.url.replace('%2C', ',')
    prepped.url = prepped.url.replace('%3A', ':')
    res = s.send(prepped)
    return json.loads(res.text)['Redirect']


# The function you actually want
def get_cached_url(url):
    payload = {
        'format': 'json',
        'no_redirect': 1,
        'q': '!cache ' + url
    }

    s = Session()
    req = Request('GET', 'https://api.duckduckgo.com', params=payload)
    prepped = s.prepare_request(req)

    # Results came back in UTF-8 so "fixing" the look of these addresses.
    prepped.url = prepped.url.replace('%21', '!')
    prepped.url = prepped.url.replace('%2C', ',')
    prepped.url = prepped.url.replace('%3A', ':')

    res = s.send(prepped)

    return json.loads(res.text)['Redirect']


# Supposed to get all the data from the cached zillow page, but I never got that far
def get_zillow_page(address):
    sleep(1)
    zillow_url = get_zillow_url(address)
    sleep(1)
    cached_url = get_cached_url(zillow_url)

    cached_url = unquote(cached_url)

    s = Session()
    req = Request('GET', cached_url)
    prepped = s.prepare_request(req)
    prepped.url = prepped.url.replace('%21', '!')
    prepped.url = prepped.url.replace('%2C', ',')
    prepped.url = prepped.url.replace('%3A', ':')
    res = s.send(prepped)

    return res.text


if __name__ == '__main__':

    for i in range(1):
        res = get_zillow_page('1120 S 2nd St APT 406, Minneapolis, MN 55415')
        print(i, res)

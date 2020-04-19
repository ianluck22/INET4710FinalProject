import rubberduck

def getCacheResponse(url):
    response = rubberduck.search(url, bang='cache', no_redirect=0, skip_disambig=0)
    result = response.content
    return result
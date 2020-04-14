from bing import getURL
from duckduckgo import getCacheResponse
from zillowProcess import getInformation
import sys, time, pickle
from tqdm import tqdm
import pandas as pd

FILE_NUMBER = sys.argv[1]

df = pickle.load(open(f"../../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft", "rb"))
list_of_addresses = df[df["zpid"] == ""]["property"].to_list()

for search_term in tqdm(list_of_addresses):
    time.sleep(5)
    url = getURL(search_term)

    if url != None:
        try:
            cacheData = getCacheResponse(url)
        except Exception as e:
            print (str(e))
            
        try:
            payload = getInformation(cacheData)
            del payload['listing_sub_type']
            for x in payload:
                df.loc[df['property'] == search_term, [x]] = payload[x]
        except Exception as e:
            print (str(e))
            


    pickle.dump(df, open(f"../../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft", "wb"))

from bing import getURL
import sys, time, pickle
from tqdm import tqdm
import pandas as pd

FILE_NUMBER = sys.argv[1]

df = pickle.load(open(f"../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft", "rb"))
list_of_addresses = df[df["ZillowURL"] == ""]["property"].to_list()

for search_term in tqdm(list_of_addresses):
    url = getURL(search_term)
    if url == None:
        df.loc[df['property'] == search_term, ['ZillowURL']] = "None"
    else:
        df.loc[df['property'] == search_term, ['ZillowURL']] = url

    pickle.dump(df, open(f"../datafiles/metroAreaChunks/metroArea{FILE_NUMBER}.ft", "wb"))

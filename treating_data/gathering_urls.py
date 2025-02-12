# currently deprecated
# this whole code needs to be updated to the 2018 100k database

import pandas as pd
import requests
import json
import config

items = pd.read_csv('../ml-100k/u.item', encoding="latin-1", delimiter="|")


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {config.TMDB_ACCESS_TOKEN}"
}

BASE_IMG_URL = "https://image.tmdb.org/t/p/w500"
poster_urls_list = list()

for index, row in items.iterrows():
    if '(' in row[1]:
        formatted_name = row[1][:row[1].index('(')].replace(" ", "%20").replace(",", "%2C").replace("'", "%27").replace("`", "%60")
    else:
        formatted_name = row[1].replace(" ", "%20").replace(",", "%2C").replace("'", "%27").replace("`", "%60")

    url = f"https://api.themoviedb.org/3/search/movie?query={formatted_name}&include_adult=true&language=en-US&page=1"



    response = requests.get(url, headers=headers)
    data = response.json()

    try:
        image_url = BASE_IMG_URL + response.json()["results"][0]["poster_path"]
    except:
        image_url = ""
    
    try:
        title = response.json()["results"][0]["original_title"]
    except:
        title = ""
    
    if title != "":
        poster_urls_list.append({"title": response.json()["results"][0]["original_title"], "poster_url": image_url})

    print(image_url)

    # print(response.text)
    # print(formatted_name)

with open("../poster_urls.json", "w", encoding="utf-8") as f:
    json.dump(poster_urls_list, f, indent=4)
    
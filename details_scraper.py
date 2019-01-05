# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 16:02:35 2019

@author: Tobi
"""
import requests
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
headers = {'User-Agent':user_agent}

# Loading in list of all games
meta_games = pd.read_csv('Data/result.csv')

meta_games.sort_values(by='metascore',ascending=False).head(20)
#np.unique(meta_games['console'])

# Making a copy of the datafram that I will mutate
meta_games_copy = meta_games.copy()

# Adding new columns for genre, publisher, etc
details = ["genre(s)","developer","players","publisher","rating"] 
extra_details = ["ESRB Descriptors:", "Number of Online Players:", "Special Controllers:", "Number of Players:"]

for new_col in details + extra_details + ['official site']:
    new_col = new_col.strip(':').lower()
    meta_games_copy[new_col] = np.empty

def URLMaker(name,platform,end=""):
    base_url = 'https://www.metacritic.com/game'
    platform_dict = {'PS':'playstation',
                    'PS2':'playstation-2',
                    'PS3':'playstation-3',
                    'PS4':'playstation-4',
                    'X360':'xbox-360',
                    'XBOX':'xbox',
                    'PC':'pc',
                    'VITA':'playstation-vita',
                    '3DS':'3ds',
                    'DC':'dreamcast',
                    'DS':'ds',
                    'GBA':'game-boy-advance',
                    'GC':'gamecube',
                    'N64':'nintendo-64',
                    'PSP':'psp',
                    'Switch':'switch',
                    'WII':'wii',
                    'WIIU':'wii-u',
                    'XONE':'xbox-one'}
    full_platform = platform_dict[platform.strip()]
    simplified_name = name.lower().strip()
    # Getting rid of junk from the title
    simplified_name = simplified_name.replace('\'','').replace(',','').replace(':','').replace('/','')
    simplified_name = simplified_name.replace('.','').replace(';','').replace('&','')
    simplified_name = simplified_name.replace(' ', '-')
    
    complete_url= '/'.join([base_url,full_platform,simplified_name,end])
    return complete_url

extra_details = ["ESRB Descriptors:", "Number of Online Players:", "Special Controllers:", "Number of Players:"]

for i, row in meta_games.iterrows():
    if i > 10:
        break
    print(row['name'], i)
    game_metacritic_url = URLMaker(row['name'], row['console'], 'details')
    try: 
        game_req = requests.get(game_metacritic_url, headers = headers)
    except:
        meta_games_copy.to_csv('extra_details_up_until_now.csv')
        time.sleep(20) 
        game_req = requests.get(game_metacritic_url, headers = headers)
    if game_req.status_code != 200:
        print(game_req.status_code,game_metacritic_url)
    else:
        details_soup = BeautifulSoup(game_req.content, 'html.parser')
        
        # Doing publisher separately, first
        publisher = details_soup.find_all('a', {'href': re.compile(r'/company')})[1].get_text().strip()
        meta_games_copy.at[i,'publisher'] = publisher
        
        
        game_details = details_soup.find_all('th', scope='row')
        for detail in game_details:
            if detail.get_text() in extra_details:
                value = detail.next_sibling.get_text().strip()
            elif detail.get_text() == "Genre(s):":
                value = detail.next_sibling.next_sibling.get_text().split(',')
                for j in range(len(value)):
                    value[j] = value[j].strip()
                value = np.unique(value)
            else:
                value = detail.next_sibling.next_sibling.get_text().strip()
            key = detail.get_text().strip(':').lower()
            meta_games_copy.at[i,key] = value 
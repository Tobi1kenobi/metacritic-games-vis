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
import sys


def URLMaker(name,platform,end=""):
    '''Makes metacritic urls from a game name and platform. Anything given as end is appended the end of the url'''
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
    simplified_name = simplified_name.replace('.','').replace(';','').replace('& ','').replace('#',',')
    simplified_name = simplified_name.replace(' ', '-')
    
    complete_url= '/'.join([base_url,full_platform,simplified_name,end])
    return complete_url

def GetFranchise(detail_soup):
    franchise_js = detail_soup.find('script', {"type":"text/javascript",
                                                    "src":"https://urs.metacritic.com/sdk/urs.js"}).previous_sibling.previous_sibling
    franchise_text = franchise_js.get_text().strip().split(';')
    for element in franchise_text:
        element = element.strip()
        if re.match(re.compile('MetaC.Video.setIMATargeting\(\"franchise*'), element):
            match = element
            match = match.split(',')[-1].strip().strip('\)').strip('\"')
            match = match.replace('-', ' ')
            return(match)

def main(stopped):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers = {'User-Agent':user_agent}
    
    # Loading in list of all games
    meta_games = pd.read_csv('../Data/result.csv')
    
    
    # Making a copy of the dataframe that I will mutate
    meta_games_copy = meta_games.copy()
    
    # Adding new columns for genre, publisher, etc
    details = ["genre(s)","developer","players","publisher","rating"] 
    extra_details = ["ESRB Descriptors:", "Number of Online Players:", "Special Controllers:", "Number of Players:"]
    
    for new_col in details + extra_details + ['official site','franchise']:
        new_col = new_col.strip(':').lower()
        meta_games_copy[new_col] = np.empty
    try:
       meta_games_copy = pd.read_csv("../Data/extra_details_up_until_now.csv",index_col=0).drop_duplicates()
    except:
        print('Could not find extra details csv')
    try:
        for i, row in meta_games[stopped:].iterrows():
            print(row['name'], i)
            game_metacritic_url = URLMaker(row['name'], row['console'], 'details')
            try: 
                game_req = requests.get(game_metacritic_url, headers = headers)
            except:
                meta_games_copy.to_csv('extra_details_up_until_now.csv')
                print("Request blocked, waiting 15 seconds.")
                time.sleep(15) 
                game_req = requests.get(game_metacritic_url, headers = headers)
            if game_req.status_code != 200:
                print(game_req.status_code,game_metacritic_url)
            else:
                details_soup = BeautifulSoup(game_req.content, 'html.parser')
                
                # Doing publisher and franchise separately, first
                try:
                    publisher = details_soup.find_all('a', {'href': re.compile(r'/company')})[1].get_text().strip()
                except:
                    publisher = np.empty
                try:
                    franchise = GetFranchise(details_soup)
                except:
                    franchise = np.empty
                meta_games_copy.at[i,'publisher'] = publisher
                meta_games_copy.at[i,'franchise'] = franchise
                
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
                        try:
                            value = detail.next_sibling.next_sibling.get_text().strip()
                        except:
                            continue
                    key = detail.get_text().strip(':').lower()
                    meta_games_copy.at[i,key] = value 
    except:
        meta_games_copy.to_csv('../Data/extra_details_up_until_now.csv')
        return('Stopped at:', i)
                
    meta_games_copy.to_csv('../Data/extra_details_complete.csv')
    return('Finished')
    
try:
    stop = int(sys.argv[1])
    main(stop)
except:
    pass


# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 21:51:55 2019

@author: Tobi
"""

import requests
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
    simplified_name = simplified_name.replace('.','').replace(';','').replace('& ','')
    simplified_name = simplified_name.replace(' ', '-')
    
    complete_url= '/'.join([base_url,full_platform,simplified_name,end])
    return complete_url


def main(stopped):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers = {'User-Agent':user_agent}
    
    # Loading in list of all games
    meta_games = pd.read_csv('../Data/result.csv')
    
    #np.unique(meta_games['console'])
    
    # Making a copy of the datafram that I will mutate
    meta_games_copy = meta_games.copy()
    
    for new_col in ['review scores', 'review summaries']:
        meta_games_copy[new_col] = np.empty
    
    
    try:
       scores_up_until_now = pd.read_csv("../Data/scores_up_until_now.csv", index_col=0)
       meta_games_copy = pd.merge(scores_up_until_now, meta_games_copy,how='outer')
    except:
        print('Could not find scores csv')
    
    try:
        for i, row in meta_games[stopped:].iterrows():
            print(row['name'], i)
            game_metacritic_url = URLMaker(row['name'], row['console'], 'critic-reviews')
            try: 
                game_req = requests.get(game_metacritic_url, headers = headers)
            except:
                meta_games_copy.to_csv('../Data/scores_up_until_now.csv')
                print("Request blocked, waiting 15 seconds.")
                time.sleep(15) 
                game_req = requests.get(game_metacritic_url, headers = headers)
            if game_req.status_code != 200:
                print(game_req.status_code,game_metacritic_url)
            else:
                reviews_soup = BeautifulSoup(game_req.content, 'html.parser')
                review_metas = reviews_soup.find_all('li', {"class":"review critic_review"})
                review_score_dict = {}
                review_summary_dict = {}
                for rev in review_metas:
                    try:
                        cur_rev_critic = rev.find('div', {"class":"review_critic"}).find('a').get_text().strip()
                    except:
                        try:
                            cur_rev_critic = rev.find('div', {"class":"review_critic"}).find('div').get_text().strip()
                        except:
                            continue
                    cur_rev_summary = rev.find('div', {"class":"review_body"}).get_text().strip()
                    cur_rev_score = rev.find('div', {"class":"review_grade"}).get_text().strip()
    
                    review_summary_dict[cur_rev_critic] = cur_rev_summary
                    review_score_dict[cur_rev_critic] = cur_rev_score
    
                    meta_games_copy.at[i,'review scores'] = review_score_dict
                    meta_games_copy.at[i, 'review summaries'] = review_summary_dict
    except:
        meta_games_copy.to_csv('../Data/scores_up_until_now.csv')
                
    meta_games_copy.to_csv('../Data/scores_complete.csv')  

try:
    stop = int(sys.argv[1])
    main(stop)
except:
    pass
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:45:40 2019

@author: Tobi
"""
import pandas as pd
import numpy as np
import json
import re
from jinja2 import Environment, FileSystemLoader
import os
import warnings
warnings.filterwarnings('ignore')

#######################################
## FUNCTIONS
#######################################
def UserGame(details):
    '''Function for taking user input'''

    possible_platforms = np.unique(details['console'])
    while(True):

        platform = input('Please provide the platform of the game in the following format\n'+', '.join(possible_platforms)+':\n')
                
        not_found_platform_msg = '\nCould not find your given platform ' +platform+ ', please ensure it is in the correct format.\n' 
        
        if platform not in possible_platforms:
            print(not_found_platform_msg)
        else:
            break
    i = 1
    console_details = details.loc[details['console']==platform]
    while(True):
        game_name = input('Please provide the full title of the game you are interested in:\n')
        
        not_found_game_msg = '\nCould not find your given input ' + game_name + ' on ' + platform + '.\nPlease ensure you use the full title as found on www.metacritic.com, it is on the specifed platform, and that the game was released between January 2000 and October 2018.'
        
        if console_details.loc[console_details['name']==game_name].empty:
            print(not_found_game_msg)
            print('Was your game one of the following?')
            first_word = game_name.split(' ')[0]
            
            if i < 3:
                match_first_word = np.unique(console_details.loc[console_details['name'].str.contains('^'+first_word+' ',case=False)]['name'].values)[(i*5)-5:i*5]
            else:
                match_first_word = np.unique(console_details.loc[console_details['name'].str.contains('^'+first_word+' ',case=False)]['name'].values)
            
            print('\n'.join(match_first_word))
            i += 1
        else:
            break
    return game_name, console_details

def GetGameFeatures(game, console_dataframe):
    '''Takes a console specific dataframe and game name as input and returns the
    relevant features of that game'''
    game_row = console_dataframe.loc[console_dataframe['name'] == game]
    franchise = list(game_row['franchise'])[0]
    developers = list(game_row['developer'])[0]
    publishers = list(game_row['publisher'])[0]
    genres = list(game_row['genre(s)'])[0]
    online_mp = list(game_row['number of online players'])[0]
    offline_mp = list(game_row['number of players'])[0]
    
    if type(franchise) != str:
        franchise = False
        
    if type(developers) == str:
        developers = developers.split(',')
    else: developers = ''
        
    if type(publishers) == str:
        publishers = publishers.split(',')
    else: publishers = ''
        
    if type(genres) == str:
        genres = genres.split(',')
    else: genres =''
        
    if type(online_mp) == str:
        if (online_mp == 'No Online Multiplayer') or (online_mp == '')or (online_mp == ' '):
            online_mp = False
        else:
            online_mp = True
    else: online_mp = False
            
    if type(offline_mp) == str:
        if (offline_mp == '1 Player') or (offline_mp == '') or (offline_mp == ' '):
            offline_mp = False
        else:
            offline_mp = True
    else: offline_mp = False
    game_features = {'genres':genres,
               'developers':developers,
               'publisher':publishers,
               'franchise':franchise,
               'online':online_mp,
               'offline':offline_mp}
    return game_features

def GetReccomendedGames(game_feat_dict, details_df):
    '''Given all the categories in a dictionary, searches a dataframe and returns all 
    rows that match for each category, including duplicates across categories'''
    franchise = game_feat_dict['franchise']
    developers = game_feat_dict['developers']
    publishers = game_feat_dict['publisher']
    genres = game_feat_dict['genres']
    offline = game_feat_dict['offline']
    online = game_feat_dict['online']
    
    if franchise != False:
        franchise_games = {franchise: details_df.loc[details_df['franchise']==franchise]}
    else: franchise_games = {'No Franchise':details_df.iloc[0:0]}
            
    dev_games = {}
    for dev in developers:
        dev_games[dev] =  details_df.loc[details_df['developer'].str.contains(dev+'(,|$)')]
        
    pub_games = {}
    for pub in publishers:
        pub_games[pub] =  details_df.loc[details_df['publisher']==pub]
    
    genre_games = {}
    for genre in genres:
        # Regex matchs either a comma following or the end of line so Action won't match Action Adventure
        genre_games[genre] =  details_df.loc[details_df['genre(s)'].str.contains(genre+'(,|$)')]

    if offline == True:
        offline_games = {'offline':details_df.loc[details_df['number of players'].str.contains('s').fillna(False)]}
    else: offline_games = {'offline':details_df.iloc[0:0]}
        
    if online == True:
        online_games = {'online':details_df.loc[details_df['number of online players'].str.contains('s').fillna(False)]}
    else: online_games = {'online':details_df.iloc[0:0]}
    
    return [franchise_games, dev_games, pub_games, genre_games, offline_games, online_games]
        
def MakeTopNLinks(source, values_df, N, already_included):
    '''Takes a category source node, a dataframe, N and a list of games that have already been used
    and returns a dictionary of links between the source and the N games with the highest metascores
    that are not in the already used list'''
    already = already_included[:]
    root = already[0]
    if values_df.empty:
        return([],already)
    topn_links = [{'source':source, 'target': root, 'distance': 50, 'strength': 0.2}]
    i = 0
    names = list(values_df['name'])
    for name in names:
        if name == root:
            continue
        elif name in already:
            link_dict = {'source':source, 'target': name, 'distance': 200, 'strength': 0.0001}
        elif i >= N:
            continue
        else:
            link_dict = {'source':source, 'target': name, 'distance': 80, 'strength': 0.001}
            already.append(name)
            i += 1
        topn_links.append(link_dict)
    return topn_links, already

def LinkMakerWrapper(game, category_games_dictionary, N = 5):
    already_list = [game]
    franchise_games, dev_games, pub_games, gen_games, off_games, on_games = category_games_dictionary
    all_leaf_nodes = []

    # Franchise then developer then publisher then genres then the two multiplayers
    for key,val in franchise_games.items():
        topn_franchise, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_franchise

    for key,val in dev_games.items():
        topn_dev, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_dev

    for key,val in pub_games.items():
        topn_pub, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_pub

    for key,val in gen_games.items():
        topn_by_gen, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_by_gen
        
    for key,val in off_games.items():
        topn_offgames, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_offgames
        
    for key,val in on_games.items():
        topn_ongames, already_list = MakeTopNLinks(key, val, N, already_list)
        all_leaf_nodes += topn_ongames
        
    return all_leaf_nodes,already_list

def MakeListOfCategories(list_category_game_dicts):
    categories_node_list = []
    for cat_game_dict in list_category_game_dicts:
        current_categories = list(cat_game_dict.keys())
        if (current_categories == ['online']) or (current_categories == ['offline']):
            if list(cat_game_dict.values())[0].empty:
                continue
        categories_node_list += current_categories
    return(categories_node_list)

def CategoryType(game_row, cat):
    if cat in ['online', 'offline']:
        return(cat)
    elif cat == 'No Franchise':
        return('franchise')
    for i, col in game_row.iteritems():
        if (type(col.values[0]) == str) and (cat in col.values[0]):
            return(i)

def MakeNodes(root_game, list_of_categories, list_of_games, details_df):
    'Makes the nodes for the graph'
    root_row = details_df.loc[details_df['name'] == root_game]
    
   
    node_group_dict = {'game':1, 'genre(s)':2,
                       'online':3,'offline':3,
                       'developer':4,'publisher':4,
                      'franchise': 5}
    level_dict = {'root game':1, 'category':2, 'leaf game':5}
    
    game_root = {'id':root_game,
                 'group':node_group_dict['game'],
                 'label':root_game,
                 'level':level_dict['root game'],
                'metascore':root_row['metascore'].values[0],
                'userscore':root_row['userscore'].values[0],
                'rating':root_row['rating'].values[0],
                'release':root_row['date'].values[0],
                'website':root_row['official site'].values[0]}
    node_list = [game_root]
    
    cat_node_list = []
    for cat in list_of_categories:
        cat_type = CategoryType(root_row.iloc[:,2:], cat)
        cat_node = {'id':cat, 'group':node_group_dict[cat_type], 'label':cat, 'level':level_dict['category']}
        cat_node_list.append(cat_node)
    node_list += cat_node_list
    
    other_game_node_list = []
    for name in list_of_games:
        if name == root_game:
            continue
        else:
            other_game_row = details_df.loc[details_df['name']==name]
            other_game_dict = {'id':name,
                             'group':node_group_dict['game'],
                             'label':name,
                             'level':level_dict['leaf game'],
                             'metascore':other_game_row['metascore'].values[0],
                             'userscore':other_game_row['userscore'].values[0],
                             'rating':other_game_row['rating'].values[0],
                             'release':other_game_row['date'].values[0],
                             'website':other_game_row['official site'].values[0]}
            other_game_node_list.append(other_game_dict)
    
    node_list += other_game_node_list
    
    return(node_list)

def main():
    # Load data
    game_details = pd.read_csv("../Data/extra_details_complete.csv",index_col=0)
    # Sort database by descending metascore
    game_details = game_details.sort_values('metascore',ascending=False)
    # Take user input for the game and platform
    game_name, console_df = UserGame(game_details)
    # Make the nodes and links
    games_features = GetGameFeatures(game_name, console_df)
    list_rec_game_dicts = GetReccomendedGames(games_features, console_df)
    links, leaf_game_list = LinkMakerWrapper(game_name, list_rec_game_dicts, 5)
    categories_list = MakeListOfCategories(list_rec_game_dicts)
    nodes = MakeNodes(game_name, categories_list, leaf_game_list, console_df)
    # Render the d3.js template with the nodes and links
    templates_dir = '../templates'
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('game_template.html')
    filename = 'game.html'
    with open(filename, 'w') as fh:
        fh.write(template.render(
            game_nodes = nodes,
            game_links = links,
        ))
    # Open the template
    os.startfile(filename)

main()

# Based on code found here
# https://bl.ocks.org/rofrischmann/0de01de85296591eb45a1dde2040c5a1



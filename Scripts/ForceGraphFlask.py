
from flask import Flask, request, redirect, url_for, make_response, render_template
import pandas as pd
import numpy as np


#######################################
## FUNCTIONS
#######################################
def BadInput(game, console, details):
    '''Function for checking user input'''

    possible_platforms = np.unique(details['console'])

    if console not in possible_platforms:
        return("console", details.iloc[0:0])

    console_details = details.loc[details['console']==console]

    not_found_game_msg = 'Could not find your given input <b>' + game + '</b> on <b>' + console + '</b>.<br/>Please ensure you use the <u>full title</u> as found on <a href =https://www.metacritic.com/game>www.metacritic.com</a>, it is on the specified platform, and that the game was released between January 2000 and October 2018.'

    if console_details.loc[console_details['name']==game].empty:
        not_found_game_msg += '<br/><br/>Was your game perhaps one of the following?<br/>'
        first_word = game.split(' ')[0]
        match_first_word = np.unique(console_details.loc[console_details['name'].str.contains('^'+first_word+' ',case=False)]['name'].values)

        not_found_game_msg += '<br/>'.join(match_first_word)
        return(not_found_game_msg, details.iloc[0:0])
    else:
        return True, console_details

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
        if (online_mp == 'No Online Multiplayer') or (online_mp == '') or (online_mp == ' '):
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


def MakeNetwork(game_name, console_df):
    '''Wrapper function for making the nodes and links'''
    games_features = GetGameFeatures(game_name, console_df)
    list_rec_game_dicts = GetReccomendedGames(games_features, console_df)
    links, leaf_game_list = LinkMakerWrapper(game_name, list_rec_game_dicts, 5)
    categories_list = MakeListOfCategories(list_rec_game_dicts)
    nodes = MakeNodes(game_name, categories_list, leaf_game_list, console_df)

    return(nodes,links)

###########################################
## FLASK
###########################################

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('homepage.html')

@app.route('/recommendations')
def entry(message='Hello'):
    return render_template('discover.html', error_message = message)


@app.route('/recommendations/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        console = request.form['console']
        game = request.form['game']
        # Load data
        game_details = pd.read_csv("extra_details_complete.csv",index_col=0)
        # Sort database by descending metascore
        game_details = game_details.sort_values('metascore',ascending=False)
        input_response, console_details = BadInput(game, console, game_details)
        if input_response == 'console':
            return entry('Console <b>'+ console + '</b> provided did not match specified input format.')
        elif type(input_response) == str:
            return entry(input_response)
        else:
            nodes,links = MakeNetwork(game, console_details)
            return NetworkGraph(nodes, links)
    else:
        return entry()


@app.route('/recommendations/graph')
def NetworkGraph(nodes,links):
    return render_template('game_template.html', game_nodes = nodes, game_links = links)






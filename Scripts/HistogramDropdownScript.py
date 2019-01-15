def main():
    from plotly.offline import init_notebook_mode, iplot
    from IPython.display import display, HTML
    from plotly.graph_objs import Histogram as H
    import plotly.graph_objs as go
    import pandas as pd
    import numpy as np
    init_notebook_mode(connected=True)
    ##########################
    # RUN THIS
    # Load data about games
    meta_games = pd.read_csv('../Data/extra_details_complete.csv')

    # make new year column and replace tbd values with np.nans
    meta_games['year'] = np.nan
    meta_games.replace('tbd', np.nan)

    # enter year value from date column
    for i, row in meta_games.iterrows():
        year_value = meta_games['date'][i].split(',')[1].strip()
        meta_games.at[i, 'year'] = int(year_value)

    # make a dict of meta_game dataframes for each year from 2000 to 2019 #irrelevant
    # meta_games_years=[]
    # for i in range(2000, 2019):
    #    meta_games_years[i] = meta_games[(meta_games['year'] == i)]

    # remove tbd and replace with nan
    meta_games = meta_games.replace('tbd', np.nan)

    # make dict for consoles
    console_dict = {}
    for console in np.unique(meta_games['console']):
        console_dict[console] = meta_games[(meta_games['console'] == console)]

    # make dict for publishers
    pub_dict = {}
    for pub in np.unique(meta_games['publisher']):
        all_by_pub = meta_games[(meta_games['publisher'] == pub)]
        if len(all_by_pub) > 20:  # only pubs with 20 games
            pub_dict[pub] = meta_games[(meta_games['publisher'] == pub)]
        # remove ' ' empty string from pub names
    pub_dict.pop(' ', None)

    # make dict for devs
    dev_dict = {}
    for dev in np.unique(meta_games['developer']):
        all_by_dev = meta_games[(meta_games['developer'] == dev)]
        if len(all_by_dev) > 20:  # only devs with 20 games
            dev_dict[dev] = meta_games[(meta_games['developer'] == dev)]
    dev_dict.pop(' ', None)

    # make dict for genre
    genre_dict = {}
    for genre in np.unique(meta_games['genre(s)']):
        all_by_genre = meta_games[(meta_games['genre(s)'] == genre)]
        if len(all_by_genre) > 100:  # only genre with 20 games
            genre_dict[genre] = meta_games[(meta_games['genre(s)'] == genre)]
    genre_dict.pop(' ', None)

    # remove wrong pc and vita console
    del console_dict[' PC']
    del console_dict[' VITA']

    ########################## Plotly plot
    import plotly.plotly as py
    import plotly.graph_objs as go
    from datetime import datetime
    import pandas as pd
    # make a user on plotly - add username and generated new api key
    import plotly
    plotly.tools.set_credentials_file(username='thomasnicolet', api_key='ln0vpFkn0fVIxOkBwpnL')

    ########################## Plot for histogram, list of traces for console, pub, dev

    # make data traces, which will be appended to data list
    # console data
    data_console = []
    for console in console_dict:
        console_metatrace = go.Histogram(
            x=console_dict[console]['metascore'],
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='metascore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#8181F7',
            ),
            opacity=0.75
        )
        console_usertrace = go.Histogram(
            x=console_dict[console]['userscore'].astype(float) * 10,
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='userscore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#FFD7E9',
            ),
            opacity=0.75
        )
        data_console.append(console_metatrace)
        data_console.append(console_usertrace)

    #### publisher data trace
    data_pub = []
    for pub in pub_dict:
        pub_metatrace = go.Histogram(
            x=pub_dict[pub]['metascore'],
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='metascore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#8181F7',
            ),
            opacity=0.75
        )
        pub_usertrace = go.Histogram(
            x=pub_dict[pub]['userscore'].astype(float) * 10,
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='userscore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#FFD7E9',
            ),
            opacity=0.75
        )
        data_pub.append(pub_metatrace)
        data_pub.append(pub_usertrace)

    ####Making dev traces
    data_dev = []
    for dev in dev_dict:
        dev_metatrace = go.Histogram(
            x=dev_dict[dev]['metascore'],
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='metascore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#8181F7',
            ),
            opacity=0.75
        )
        dev_usertrace = go.Histogram(
            x=dev_dict[dev]['userscore'].astype(float) * 10,
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='userscore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#FFD7E9',
            ),
            opacity=0.75
        )
        data_dev.append(dev_metatrace)
        data_dev.append(dev_usertrace)

    # make data trace for genre
    data_genre = []
    for genre in genre_dict:
        genre_metatrace = go.Histogram(
            x=genre_dict[genre]['metascore'],
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='metascore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#8181F7',
            ),
            opacity=0.75
        )
        genre_usertrace = go.Histogram(
            x=genre_dict[genre]['userscore'].astype(float) * 10,
            ##ADD/REMOVE HISTNORM FOR NORMALISING
            histnorm='percent',
            name='userscore',
            xbins=dict(
                start=0,
                end=100,
                size=5
            ),
            marker=dict(
                color='#FFD7E9',
            ),
            opacity=0.75
        )
        data_genre.append(genre_metatrace)
        data_genre.append(genre_usertrace)

    ### make a list with all lists of data traces
    total_data = data_console + data_pub + data_dev + data_genre

    # big_bool list is length of all data traces, list of list of bools, where every list consists of
    # len(total_data) of falses, where every list has a pair of True, shifted by two for every list.
    empty_big_bool = len(total_data) * [False]
    big_bool = []
    for i in range(0, len(total_data), 2):
        temp_big_bool = len(total_data) * [False]
        temp_big_bool[i] = True
        temp_big_bool[i + 1] = True
        big_bool.append(temp_big_bool)

    #
    # making list of dictionaries to be used as argument for buttons in updatemenus
    # console
    buttons_console_list = []
    for i in list(range(0, len(console_dict))):
        temp_list = dict(label=list(console_dict)[i],
                         method='update',
                         args=[{'visible': big_bool[0:len(console_dict)][i]},
                               {'title': "console: " + list(console_dict)[i]}])
        buttons_console_list.append(temp_list)

    #### publisher
    buttons_pub_list = []
    for i in list(range(0, len(pub_dict))):
        temp_list = dict(label=list(pub_dict)[i],
                         method='update',
                         args=[{'visible': big_bool[len(console_dict):len(console_dict) + len(pub_dict)][i]},
                               {'title': list(pub_dict)[i]}])
        buttons_pub_list.append(temp_list)

    ### developer
    buttons_dev_list = []
    for i in list(range(0, len(dev_dict))):
        temp_list = dict(label=list(dev_dict)[i],
                         method='update',
                         args=[{'visible': big_bool[
                                           len(console_dict) + len(pub_dict):len(console_dict) + len(pub_dict) + len(
                                               dev_dict)][i]},
                               {'title': list(dev_dict)[i]}])
        buttons_dev_list.append(temp_list)

    # genre
    buttons_genre_list = []
    for i in list(range(0, len(genre_dict))):
        temp_list = dict(label=list(genre_dict)[i],
                         method='update',
                         args=[{'visible': big_bool[len(console_dict) + len(pub_dict) + len(dev_dict):][i]},
                               {'title': list(dev_dict)[i]}])
        buttons_genre_list.append(temp_list)

    # make update menus. buttons is made up of buttons_list, i.e. list of dictionaries containing label, method, args and title.
    # args variable determines when what is being shown, e.g. [True, False False... False] means first is being shown only
    button_layer_1_height = 1.12
    updatemenus = list([
        dict(
            active=-1,
            buttons=buttons_console_list,
            name='Console',
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=False,
            x=0,
            xanchor='left',
            y=button_layer_1_height,
            yanchor='top'
        ),
        dict(
            active=-1,
            buttons=buttons_pub_list,
            name='Publisher',
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=False,
            x=0.1,
            xanchor='left',
            y=button_layer_1_height,
            yanchor='top'
        ),
        dict(
            active=-1,
            buttons=buttons_dev_list,
            name='Developer',
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=False,
            x=0.35,
            xanchor='left',
            y=button_layer_1_height,
            yanchor='top'
        ),
        dict(
            active=-1,
            buttons=buttons_genre_list,
            name='Developer',
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=False,
            x=0.755,
            xanchor='left',
            y=button_layer_1_height,
            yanchor='top'
        )
    ])

    # set layout
    layout = dict(title='Userscores and metascores across platform, publisher, developer and genre',
                  showlegend=False,
                  width=1400,
                  height=650,
                  yaxis=dict(
                      range=[0, 40],
                      title='Count'
                  ),
                  xaxis=dict(
                      range=[0, 100],
                      title='Userscore and metascores'
                  ),
                  updatemenus=updatemenus)
    # plot figure
    fig = dict(data=total_data, layout=layout)
    py.iplot(fig, filename='update_dropdown')

main()
def main():
    from plotly.offline import init_notebook_mode, iplot
    from IPython.display import display, HTML
    from plotly.graph_objs import Histogram as H
    import plotly.graph_objs as go
    import pandas as pd
    import numpy as np
    init_notebook_mode(connected=True)

    ### data loading
    meta_games = pd.read_csv('../Data/extra_details_complete.csv')

    # make new year column and replace tbd values with np.nans
    meta_games['year'] = np.nan
    meta_games.replace('tbd', np.nan)

    # enter year value from date column
    for i, row in meta_games.iterrows():
        year_value = meta_games['date'][i].split(',')[1].strip()
        meta_games.at[i, 'year'] = int(year_value)

    meta_games = meta_games.replace('tbd', np.nan)
    meta_games_years = {}

    # make a dict of meta_game dataframes for each year from 2000 to 2019
    for i in range(2000, 2019):
        meta_games_years[i] = meta_games[(meta_games['year'] == i)]

    meta_games.head(5)

    ### making histogram
    # Plotting meta_games data as histogram, both user-and metascores per year, with a slider.
    years = list(range(2000, 2019))

    # make figure
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }

    # fill in most of layout
    figure['layout']['xaxis'] = {'range': [0, 100], 'title': 'Scores'}
    figure['layout']['yaxis'] = {'range': [0, 220], 'title': 'Count'}
    figure['layout']['title'] = 'Metascore and userscore of video games 2000-2018'
    figure['layout']['bargap'] = 0.1
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['sliders'] = {
        'args': [
            'transition', {
                'duration': 400,
                'easing': 'elastic'  # changed "cubic-in-out"
            }
        ],
        'initialValue': '2000',
        'plotlycommand': 'animate',
        'values': years,
        'visible': True
    }
    figure['layout']['updatemenus'] = [
        {
            # REMOVED BUTTONS HERE

            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]

    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'elastic'},  # changed cubic-in-out
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }

    # make data
    year = 2000
    userscore_raw2000 = (meta_games_years[2000]['userscore'])
    userscore_list2000 = np.sort(userscore_raw2000.astype(np.float) * 10)
    meta_games_by_year = meta_games[meta_games['year'] == year]
    userscore_list_nonan2000 = []
    for score in userscore_list2000:
        if not np.isnan(score):
            userscore_list_nonan2000.append(int(score))

    # 2 datadicts which are put into figure['data'], like trace 1 and 2
    data_dict_2000meta = H({
        'x': list(meta_games_by_year['metascore']),  # changed _and_cont
        # 'histnorm': 'percent',
        "histfunc": "count",
        'name': "metascore",
        'xbins': dict(
            start=0,
            end=100,
            size=5
        ),
        'marker': dict(
            color='#8181F7'
        )
    })
    figure['data'].append(data_dict_2000meta)

    data_dict_2000user = H({
        'x': userscore_list2000,
        # 'histnorm': 'percent',
        'histfunc': 'count',
        'name': "userscore",
        'xbins': dict(
            start=0,
            end=100,
            size=5
        ),
        'marker': dict(
            color='#EB89B5'
        )
    })
    figure['data'].append(data_dict_2000user)

    # make frames for histogram slider
    for year in years:
        frame = {'data': [], 'name': str(year)}
        meta_games_by_year = meta_games[meta_games['year'] == year]
        data_dict1 = H({
            'x': list(meta_games_by_year['metascore']),
            # 'histnorm': 'percent',
            'histfunc': 'count',
            'name': "metascore",
            'xbins': dict(
                start=0,
                end=100,
                size=5
            ),
            'marker': dict(
                color='#8181F7'
            )
        })

        # list of userscores as float, sorted and as floats
        userscore_raw = (meta_games_years[year]['userscore'])
        userscore_list = np.sort(userscore_raw.astype(np.float) * 10)  # I guess sort is useless in a hist
        data_dict2 = H({
            'x': userscore_list,
            # 'histnorm': 'percent',
            'histfunc': 'count',
            'name': "userscore",
            'xbins': dict(
                start=0,
                end=100,
                size=5
            ),
            'marker': dict(
                color='#EB89B5'
            )
        })

        frame['data'].append(data_dict1)
        frame['data'].append(data_dict2)

        figure['frames'].append(frame)
        slider_step = {'args': [
            [year],
            {'frame': {'duration': 300, 'redraw': False},
             'mode': 'immediate',

             'transition': {'duration': 300}}
        ],
            'label': year,
            'method': 'animate'}
        sliders_dict['steps'].append(slider_step)

    figure['layout']['sliders'] = [sliders_dict]

    iplot(figure)


main()
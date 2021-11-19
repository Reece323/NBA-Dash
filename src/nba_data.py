import os
import re
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguestandings

from src.team_colors import team_colors

table_cols = ['Rk', 'Team', 'Record', 'PCT', 'GB', 'Home', 'Away', 'Div',  
                    'PPG', 'Opp PPG', 'Diff', 'Strk', 'Last 10']

def conf_table_cols(conference):
    if conference == 'League':
        conference = 'Conference'

    cols = table_cols[:]
    cols.insert(8, f'{conference}')
    
    return cols

def conf_table_data(season, conference):
    #! add in playoff string reading for previous years after this works for current year
    url = f'https://www.espn.com/nba/standings/_/season/{int(season) + 1}'

    if conference == 'League':
        url += '/group/league'
    
    dfs = pd.read_html(url)
    time.sleep(1)

    flatten = lambda t: [item for sublist in t for item in sublist]
    start_cols = ['Rank', 'Team', 'Record', 'PCT', 'GB', 'HOME', 'AWAY', 'DIV', 'CONF', 'PPG', 'OPP PPG',
            'DIFF', 'STRK', 'L10']
    
    if conference == 'West':
        val = 3
    else:
        val = 1

    conf = dfs[val]

    teams = pd.DataFrame([dfs[val - 1].columns.values.tolist()[0]] + flatten(dfs[val - 1].values.tolist()))
    
    def playoff_str(x):
        if str(x)[5].isdigit() and str(x)[6].islower():
            return str(x)[6:8]
        elif str(x)[5].islower():
            return str(x)[5:7]
        else:
            return ''

    playoff_str_vals = teams.apply(playoff_str, axis=1)
    teams = pd.DataFrame([item.split(' ')[-1] for sublist in teams.values for item in sublist])

    teams = teams.replace({0:{i.split(' ')[-1]: i for i in list(team_colors.keys())}})
    teams['t'] = playoff_str_vals
    teams = teams.apply(lambda row: row[0] + ' -' + row['t'] if row['t'] != '' else row[0], axis=1)

    conf['Team'] = teams.apply(lambda x: x[:-1] if x.endswith(' ') else x)
    conf['PCT'] = round(conf['PCT'] * 100, 2).astype(str) + '%'
    conf['Record'] = conf['W'].astype(str) + '-' + conf['L'].astype(str)
    conf['Rank'] = range(1, len(conf) + 1)

    for j in ['PPG', 'OPP PPG', 'DIFF']:
        conf[j] = round(conf[j], 1)
        conf[j] = conf[j].astype(str)
    
    conf = conf.reindex(columns=start_cols).copy()
    conf.columns = conf_table_cols(conference)

    return conf.copy()

#%%


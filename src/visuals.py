import os
import re
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguestandings

scatter_vals = ['Team', 'Average Age', 'Wins', 'Losses', 'Pythagorean Wins', 'Pythagorean Losses', 
                'Margin of Victory', 'Strength of Schedule', 'Simple Rating System', 'Offensive Rating', 
                'Defensive Rating', 'Net Rating', 'Pace', 'Free Throw Attempt Rate', '3 Point Attempt Rate', 
                'True Shooting Percentage', 'Effective Field Goal Percentage', 'Turnover Percentage', 
                'Offensive Rebound Percentage', 'Free Throws Per Field Goal Attempt', 
                'Effective Field Goal Percentage Allowed', 'Opponent Turnover Percentage', 
                'Defensive Rebound Pecentage', 'Opponent Free Throws Per Field Goal Attempt', 'Attendance', 
                'Attendance Per Game']

def scatter_data(season):
    html = requests.get(f'http://www.basketball-reference.com/leagues/NBA_{int(season) + 1}.html').content
    time.sleep(1)
    cleaned_soup = BeautifulSoup(re.sub(rb"<!--|-->",rb"", html), features='lxml')
    misc_table = cleaned_soup.find('table', {'id':'advanced-team'})

    df = pd.read_html(str(misc_table))[0]
    df.columns = df.columns.get_level_values(1)
    df['Team'] = df['Team'].apply(lambda x: x if x[-1] != '*' else x[:-1])

    df = df.drop(['Rk', 'Arena', 'Unnamed: 27_level_1', 'Unnamed: 17_level_1', 'Unnamed: 22_level_1'], axis=1).copy()

    df.columns = scatter_vals
    
    df = df[df['Team'] != 'League Average']
    df[['Wins', 'Losses']] = df[['Wins', 'Losses']].astype(int)

    return df

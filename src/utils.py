import sys
import warnings
from datetime import datetime

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html

from src.figure_styles import center_style2

dropdown = dcc.Dropdown(
               id='season_val',
               options=[
                   {'label': str(i) + "-" + str(i + 1)[2:] + ' Season', 'value': i}
                   for i in range(2012, 2022)],
               value='2021',
               style={
                'color': 'black',
                'width':'10rem',
                'margin-right': '4rem',
                'textAlign': 'center',
                'fontSize': '.9rem'
               }
)

update = dbc.Row(
    html.H6(
        children=f'Last Updated: {datetime.now().strftime("%-I:%M:%S %p")} CST',
        style={
                'color': 'rgb(180,180,180)',
                'width':'80%',
                'padding-top' : '4%',
                'padding-left': '0%',
                'margin-right': '8rem',
                'textAlign': 'center',
                'fontSize': '.8rem'
               }
    )
)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dropdown),
        dbc.NavItem(update),
        dbc.NavItem(dbc.NavLink("League Ranks", href="/league")),
        dbc.NavItem(dbc.NavLink("Players", href="/player-games")),
    ],
    className='navbar navbar-expand-lg navbar-dark bg-transparent',
    brand="NBA Stats Dashboard",
    brand_style={
        'font-family': '"Architects Daughter", cursive',
        'font-size':'2rem'
    },
    style={'border':'none'},
    dark=True,
)

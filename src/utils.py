import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("League Ranks", href="/league")),
        dbc.NavItem(dbc.NavLink("Players", href="/player-games")),
    ],
    className='navbar navbar-expand-lg navbar-dark bg-primary',
    brand="NBA Stats Dashboard",
    brand_style={
        'font-family': '"Architects Daughter", cursive'
    },
    color="dark",
    dark=True,
)
import sys
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table as dt
from dash import dcc, html
from dash.dependencies import Input, Output

from figure_styles import center_style, center_style2, conf_table_params, table_params
from nba_data import (conf_table_cols, conf_table_data, scatter_data,
                      scatter_vals, team_colors)

import warnings
warnings.filterwarnings('ignore')


def playoff_splitter(x): return [j.rsplit(' -')[0] for j in x['Team'].values]


show_playoff_markers = False

playoff_markers = [
    html.H2('Conference clinched: -z'),
    html.H2('Division clinched: - y'),
    html.H2('Playoff spot clinched: - x'),
    html.H2('Missed Playoffs: - e')
] if show_playoff_markers else []


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server


app.layout = html.Div([
    dbc.Row(
        html.H1(
            children='NBA Stats Dashboard',
            style={'textAlign': 'center',
                'margin-top': '3rem',
                'margin-bottom': '0rem',
                'font-family': '"Architects Daughter", cursive'
                
                })
    ),

    html.Div([
        dcc.Dropdown(
            id='season_val',
            options=[{
                'label': str(i) + "-" + str(i + 1)[2:] + ' Season',
                'value': i
            } for i in range(2012, 2022)],
            value='2021'
        )
    ],
        style={ 
        'margin-top': '2rem',
        'padding-left': '40%',
        'padding-right': '40%',
        'textAlign': 'center',
        'fontSize': '1rem'
    }),

    dbc.Row(
        html.H6(
            children=f'Last Updated: {datetime.now().strftime("%-I:%M:%S %p")} CST',
            style=center_style2
        )
    ),
    html.Br(),

    dbc.Row(
        html.H2(
            children='Western Conference',
            style=center_style
        )
    ),
    dbc.Row(
        children=playoff_markers,
        style=center_style
    ),
    html.Center([
        html.Div([
            dt.DataTable(
                id='west_table',
                columns=[{
                    "name": i,
                    "id": i
                } for i in conf_table_cols('West')],
                **conf_table_params
            )
        ])
    ]),

    html.Br(),
    dbc.Row(
        html.H2(
            children='Eastern Conference',
            style=center_style
        )
    ),
    dbc.Row(
        children=playoff_markers,
        style=center_style
    ),
    html.Center([
        html.Div([
            dt.DataTable(
                id='east_table',
                columns=[{
                    "name": i,
                    "id": i
                } for i in conf_table_cols('East')],
                **conf_table_params
            )
        ])
    ]),
    html.Br(),

    dbc.Row(
        html.H2(
            children='League Statistics Comparison',
            style=center_style
        )
    ),
    dbc.Row(
        children=[
            html.H4('Choose two metrics to compare how the league stacks up!')],
        style=center_style
    ),
    html.Center(
        [dcc.Graph(id='scatter1')]
    ),

    html.Div([
        dcc.Dropdown(
            id='scatter1-x',
            options=[{
                'label': i,
                'value': i
            } for i in scatter_vals[1:]],
            value='Offensive Rating'
        )
    ],
        style={
            'fontSize': '1rem',
            'width': '50%',
            'padding-left': '25%',
            'display': 'inline-block',
            'textAlign': 'center'
    }),

    html.Div([
        dcc.Dropdown(
            id='scatter1-y',
            options=[{
                'label': i,
                'value': i
            } for i in scatter_vals[1:]],
            value='Defensive Rating'
        )
    ],
        style={
            'fontSize': '1rem',
            'width': '50%',
            'padding-right': '25%',
            'float': 'right',
            'display': 'inline-block',
            'textAlign': 'center'
    }),

    dbc.Row(
        html.H2(
            children='Power Rankings',
            style=center_style
        )
    ),
    dbc.Row(
        children=playoff_markers,
        style=center_style
    ),
    html.Center([
        html.Div([
            dt.DataTable(
                id='league_table',
                columns=[{
                    "name": i,
                    "id": i
                } for i in conf_table_cols('Conference')],
                **table_params,
            )
        ])
    ],  className='mx-5'
    ),
])


@app.callback(
    Output('east_table', 'data'),
    [Input('season_val', 'value')]
)
def update_east_table(season_val):
    east = conf_table_data(season=season_val, conference='East')
    return east.to_dict(orient='rows')


@app.callback(
    Output('west_table', 'data'),
    [Input('season_val', 'value')]
)
def update_west_table(season_val):
    west = conf_table_data(season=season_val, conference='West')

    return west.to_dict(orient='rows')


@app.callback(
    Output('league_table', 'data'),
    [Input('season_val', 'value')]
)
def update_league_table(season_val):
    league = conf_table_data(season=season_val, conference='League')

    return league.to_dict(orient='rows')


@app.callback(
    Output('scatter1', 'figure'),
    [
        Input('season_val', 'value'),
        Input('scatter1-x', 'value'),
        Input('scatter1-y', 'value')
    ]
)
def update_scatter1(season_val, x, y):
    scatter_df = scatter_data(season_val)

    scatter_to_flip = ['Defensive Rating', 'Turnover Percentage',
                       'Effective Field Goal Percentage Allowed',
                       'Opponent Free Throws Per Field Goal Attempt']

    return {
        'data': [
            go.Scatter(
                x=scatter_df[x],
                y=scatter_df[y],
                mode='markers',
                marker=dict(color=[team_colors[i][0] for i in playoff_splitter(scatter_df)],
                            size=12,
                            line=dict(
                    width=3,
                    color=[team_colors[i][1]
                            for i in playoff_splitter(scatter_df)]
                )
                ),
                hovertemplate=scatter_df['Team'].astype(str) +
                f'<br><b>{x}</b>: ' + scatter_df[x].astype(str) + '<br>' +
                f'<b>{y}</b>: ' + scatter_df[y].astype(str) + '<br>' +
                '<extra></extra>'
            )
        ],
        'layout': go.Layout(
            plot_bgcolor='#e6e6e6',
            height=750,
            width=750,
            showlegend=False,
            xaxis=dict(
                title=x,
                autorange='reversed' if x in scatter_to_flip else True
            ),
            yaxis=dict(
                title=y,
                autorange='reversed' if y in scatter_to_flip else True
            ),
            hovermode="closest",
            shapes=[
                dict(
                    type='line',
                    x0=scatter_df[x].mean(),
                    y0=scatter_df[y].min(
                    ) - ((scatter_df[y].max() - scatter_df[y].min()) * (1/15)),
                    x1=scatter_df[x].mean(),
                    y1=scatter_df[y].max(
                    ) + ((scatter_df[y].max() - scatter_df[y].min()) * (1/15)),
                    line=dict(
                        color='black',
                        width=2
                    )
                ),
                dict(type='line',
                     x0=scatter_df[x].min(
                     ) - ((scatter_df[x].max() - scatter_df[x].min()) * (1/15)),
                     y0=scatter_df[y].mean(),
                     x1=scatter_df[x].max(
                     ) + ((scatter_df[x].max() - scatter_df[x].min()) * (1/15)),
                     y1=scatter_df[y].mean(),
                     line=dict(
                         color='black',
                         width=2
                     )
                     )
            ]
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)

import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from plots import plotUCL

### LAYOUT
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph', figure=plotUCL(), config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False))],
            width=9
        ),
        dbc.Col(
            [],
            width=3
        )
    ])
], fluid=True)
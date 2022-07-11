import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from plots import plotUCL
from tables import get_oil_tbl

### LAYOUT
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph', figure=plotUCL(), config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False))
            ],
            width=9
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Label("Plot Configuration"),
                    dcc.Dropdown(
                        id="pirep-plot-dropdown",
                        options=[
                            {"label": "PK-PWA", "value": "PK-PWA"},
                            {"label": "PK-PWC", "value": "PK-PWC"}
                        ]
                    )
                ])
            ])
        ],
        width=3)
    ], class_name="pt-3")
], fluid=True)
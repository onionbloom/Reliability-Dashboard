import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

raw_tbl = pd.read_csv("csv_data_files/699235.csv")
llp_table = dash_table.DataTable(
    
)

### LAYOUT
layout = dbc.Container([
    dbc.Row([
        html.H5("ENGINE LLP STATUS", className="fw-bold text-center", style={"color": "#013764"})
    ], class_name="pt-3"),
    dbc.Row([
        dbc.Col([llp_table])
    ])
], fluid=True)
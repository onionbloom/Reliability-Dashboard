# app.py
import dash_bootstrap_components as dbc # dbc v1.1.0 gets access to Bootstrap v5.1.3
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output

import pandas as pd

from pages import page1, page2, page3

#### Instantiate Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)
server = app.server
LOGO = "./assets/PAS_Logo.png"

#### TEMPLATE LAYOUT
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Navbar(
                    dbc.Container([
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src=LOGO, height="30px"))
                                ]
                            )
                        ),
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink("Fleet Reliability Dashboard",id="dash-link", href="/dashboard")),
                            dbc.NavItem(dbc.NavLink("AD, SB Management",id="techpub-link", href="/techpub")),
                            dbc.NavItem(dbc.NavLink("PIREP Analysis", id="pirep-link", href="pirep"))
                        ], 
                        navbar=True)
                    ], fluid=True)
                )
            ])
        ],
        class_name="pt-3")
    ], fluid=True),
    html.Div(id='page-content')
])

### CALLBACK
@callback(
    Output('page-content', 'children'),
    Output('dash-link', 'active'),
    Output('techpub-link', 'active'),
    Input('url','pathname'))
def display_page(pathname):
    if pathname == '/dashboard':
        return page1.layout, True, False
    elif pathname == '/techpub':
        return page2.layout, False, True
    elif pathname == '/pirep':
        return page3.layout, False, False
    else:
        return page1.layout, True, False

if (__name__ == '__main__'):
    app.run_server(debug=True)
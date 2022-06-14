# app.py
from dash import Dash, dcc, html, ctx, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc # dbc v1.1.0 gets access to Bootstrap v5.1.3


import pandas as pd

from cards import card_tia, card_dr, card_FC, card_FH, card_del, card_cotd
from plots import plotFl, plotRem, plotOil, plotDel

# Instantiate Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

raw_ad = pd.read_excel("C:/Users/moeab/OneDrive/Documents/Work/Pelita/Documents and Publications/AD/AD biweekly report/AD Biweekly.xlsx")
df_ad = raw_ad.drop(columns=['Source.Name', 'ATA', 'RECEIVED DATE', 'ISSUE DATE', 'EFFECTIVE DATE', 'BIWEEKLY NUMBER', 'PIC', 'EVALUATION DATE', 'TC HOLDER', 'AC TYPE', 'SUBJECT', 'SUPERSEDES', 'REFERENCE', 'AFFECTED PART', 'METHOD OF COMPLIANCE', 'COMPLIANCE TIME', 'REPEAT INTERVAL', 'EFFECTIVITY', 'PARTS PROHIBITION', 'ENGINEERING ACTION'])
dff = df_ad[df_ad['TDE NUMBER'].notna()]

ad_table = dash_table.DataTable(
    dff.to_dict('records'), 
    [{'name': 'PUBLICATION NO.', 'id': 'PUBLICATION NO.'}, {'name': 'TDE STATUS', 'id': 'TDE STATUS'}],
    style_cell={
        'font-family': 'Segoe UI,-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
        'font-size': '0.75rem',
        'text-align': 'center',
    },
    style_header={
        'font-weight': 'bold'
    },
    page_current=0,
    page_size=10,
    page_action='custom',
    id='paginated-table'
    )

# Build the app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Fleet Reliability Dashboard", active=True, href="#")),
                dbc.NavItem(dbc.NavLink("AD, SB Management", href="#"))
            ], 
            pills=True, fill=True, style={"color": "#2F3B47"})
        ])
    ],
    class_name="pt-3"),

    dbc.Row([
        dbc.Col([card_dr], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_FH], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_FC], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_del], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_cotd], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_tia], class_name='d-flex justify-content-center', width=2)
    ],
    class_name="pt-3"),

    dbc.Row([
        dbc.Col([
            html.H5("AD/SB Management", className="fw-bold text-center", style={"color": "#2F3B47"}),
            dbc.Card([
                dbc.CardBody([ad_table])
            ])
        ],width=3),
        dbc.Col([
            dcc.Graph(id='graph')
        ],width=6),
        dbc.Col([
            html.H5("Plot Selection", className="fw-bold text-center", style={"color": "#2F3B47"}),
            dbc.Accordion([
                dbc.AccordionItem([
                    dbc.RadioItems(
                        options=[
                            {"label": "Oil Consumption", "value": "oil_consum"},
                            {"label": "Engine Vibration", "value": "vib"},
                            {"label": "EGT Margin", "value": "egtm"}
                            ], id="engine-radio"
                    )
                ], title="Engine Health and Monitoring"),

                dbc.AccordionItem([
                    dbc.RadioItems(
                        options=[
                            {"label": "Top 5 Delays", "value": "top5_del"},
                            {"label": "Top 5 Removals", "value": "top5_rem"},
                            {"label": "Top 5 PIREP", "value": "top5_pirep"}
                        ], id="top5-radio"
                    )
                ], title="Top 5 Summaries"),

                dbc.AccordionItem([
                    dbc.RadioItems(
                        options=[
                            {"label": "Dispatch Reliability", "value": "dr"},
                            {"label": "TIA Rate", "value":"tia"},
                            {"label": "COTD", "value":"cotd"}
                        ], id="metrics-radio"
                    )
                ], title="Reliability Metrics")
            ]),
        ], width=3)
    ],
    class_name="pt-3")   
])

@app.callback(
    Output('graph', 'figure'),
    Input('engine-radio', 'value'),
    Input('top5-radio', 'value'),
    Input('metrics-radio', 'value')
)
def update_graph(engineVal, topVal, metricsVal):
    triggered_id = ctx.triggered_id

    if triggered_id == "engine-radio":
        fig = plotOil()
    
    elif triggered_id == "top5-radio":
        if topVal == "top5_del":
            fig = plotDel()
        elif topVal == "top5_rem":
            fig = plotRem()
        else:
            fig = plotFl()
    else:
        fig = plotFl()
    
    return fig

@app.callback(
    Output('paginated-table','data'),
    Input('paginated-table', "page_current"),
    Input('paginated-table', "page_size")
)
def update_table(page_current, page_size):
    return dff.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')

if (__name__ == '__main__'):
    app.run_server(debug=True)
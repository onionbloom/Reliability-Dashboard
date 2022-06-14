from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from cards import card_tia, card_dr, card_FC, card_FH, card_del, card_cotd, card_status
from plots import plotFl, plotRem, plotOil, plotDel, plotSI
from calculations import get_status

### LAYOUT
layout = dbc.Container([
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
            html.H5("Aircraft Status", className="fw-bold text-center", style={"color": "#2F3B47"}),
            card_status
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
                            {"label": "Severity Index", "value":"si"},
                            {"label": "COTD", "value":"cotd"}
                        ], id="metrics-radio"
                    )
                ], title="Reliability Metrics")
            ]),
        ], width=3)
    ],
    class_name="pt-3")   
])

### CALLBACKS
@callback(
    Output('graph', 'figure'),
    Output('engine-radio', 'value'),
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
        if metricsVal == "dr":
            fig = plotFl()
        elif metricsVal == "si":
            fig = plotSI()
        else:
            fig = plotFl()
    
    return fig, " "

@callback(
    Output('status-model', 'children'),
    Output('status-msn', 'children'),
    Output('status-wv', 'children'),
    Output('status-status', 'children'),
    Output('status-fh', 'children'),
    Output('status-fc', 'children'),
    Input('status-dropdown', 'value')
)
def update_status(value):
    status = get_status()
    filtered = status[status['REGISTRATION'] == value]

    if len(filtered) > 0:
        return [
            filtered['AIRCRAFT TYPE'].item(), 
            format(filtered['MSN'].item(),"05d"), # Format to include a leading zero and 5 character integer digit 
            str(filtered['WEIGHT VARIANT'].item()), # Format to string
            filtered['STATUS'].item(), 
            format(filtered['CURR_TOTAL_HOURS'].item(), ",.2f"), # Format to 2 decimal places and thousands separator 
            format(filtered['CURR_TOTAL_CYCLES'].item(), ",.0f") # Format to 0 decimal places and thousands separator
        ]
    else:
        return ["N/A"] * 6
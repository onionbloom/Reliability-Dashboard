from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from cards import card_tia, card_dr, card_FC, card_FH, card_del, card_cotd, card_status
from plots import plotFl, plotRem, plotOil, plotDel, plotSI, plotCOTD
from calculations import get_status

### LAYOUT
layout = dbc.Container([
    # Row of Cards
    dbc.Row([
        dbc.Col([
            card_dr,
            dbc.Tooltip("Year-to-date Dispatch Reliability", target="card-dr", placement="bottom")
            ], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_FH], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_FC], class_name='d-flex justify-content-center', width=2),
        dbc.Col([
            card_del,
            dbc.Tooltip("Total number of delays", target="card-del", placement="bottom")
            ], class_name='d-flex justify-content-center', width=2),
        dbc.Col([
            card_cotd,
            dbc.Tooltip("Year-to-date rate of Contribution of Technical Delays", target="card-cotd", placement="bottom")
            ], class_name='d-flex justify-content-center', width=2),
        dbc.Col([card_tia], class_name='d-flex justify-content-center', width=2)
    ],
    class_name="pt-3"),
    
    # Row of Graphics
    dbc.Row([
        dbc.Col([
            html.H5("Aircraft Status", className="fw-bold text-center", style={"color": "#013764"}),
            card_status
        ],width=3),
        dbc.Col([
            dcc.Graph(id='graph', config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False))
        ],width=6),
        dbc.Col([
            html.H5("Plot Selection", className="fw-bold text-center", style={"color": "#013764"}),
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
                    ),
                    dbc.Label("Plot Configuration"),
                    dbc.Checklist(
                        options=[
                            {"label": "Weekly", "value": True}
                        ],
                        switch=True,
                        id="config-switch",
                        value=[]
                    ),
                    dbc.Tooltip("Toggle to display a weekly graph", target="config-switch")
                ], title="Reliability Metrics")
            ]),
        ], width=3)
    ],
    class_name="pt-3")   
], fluid=True)

### CALLBACKS
# Plots Callback
@callback(
    Output('graph', 'figure'),
    Output('engine-radio', 'value'),
    Output('top5-radio', 'value'),
    Output('metrics-radio', 'value'),
    Input('engine-radio', 'value'),
    Input('top5-radio', 'value'),
    Input('metrics-radio', 'value'),
    State('config-switch', "value")
)
def update_graph(engineVal, topVal, metricsVal, switch):
    triggered_id = ctx.triggered_id

    if triggered_id == "engine-radio":
        fig = plotOil()
    
    elif triggered_id == "top5-radio":
        if topVal == "top5_del":
            fig = plotDel()
        elif topVal == "top5_rem":
            fig = plotRem()
        else:
            fig = plotFl(switch)
    else:
        if metricsVal == "dr":
            fig = plotFl(switch)
        elif metricsVal == "si":
            fig = plotSI(switch)
        else:
            fig = plotCOTD(switch)
    
    return fig, " ", " ", " "
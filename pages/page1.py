from dash import dcc, html, dash_table, ctx, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme

from cards import card_tia, card_dr, card_FC, card_FH, card_del, card_cotd, card_status
from plots import plotFl, plotRem, plotOil, plotDel, plotSI, plotCOTD, plot5PIREP
from tables import get_oil_tbl

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
            dcc.Graph(id='graph', config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False)),
            dash_table.DataTable(
                id='oil-table',
                style_cell={
                'font-family': 'Segoe UI,-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
                'font-size': '0.75rem',
                'text-align': 'center',
                },
                style_header={
                    'font-weight': 'bold'
                },
            ),
        ],width=6),
        dbc.Col([
            html.H5("Plot Selection", className="fw-bold text-center", style={"color": "#013764"}),
            dbc.Accordion([
                dbc.AccordionItem([
                    dcc.Dropdown(
                        id='dropdown-ehm',
                        options=[
                            {"label": "PK-PWA", "value": "PK-PWA"},
                            {"label": "PK-PWC", "value": "PK-PWC"}
                        ],
                        value='PK-PWA'
                    ),
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
    Output('oil-table','data'),
    Output('oil-table', 'columns'),
    Input('engine-radio', 'value'),
    Input('top5-radio', 'value'),
    Input('metrics-radio', 'value'),
    State('config-switch', 'value'),
    State('dropdown-ehm', 'value'),
)
def update_graph(engineVal, topVal, metricsVal, switch, dropdown):
    triggered_id = ctx.triggered_id

    tbl = None
    columns = None
    if triggered_id == "engine-radio":
        fig = plotOil(dropdown)
        tbl = get_oil_tbl(dropdown)
        columns = [
                    dict(id='DATE', name='DATE'),
                    dict(id='ENG1_OIL', name='ENG1 Oil (Qt)'),
                    dict(id='ENG1_OIL_QTZ/FH', name='ENG1 Consumption (Qt/Hr)', type='numeric', format=Format(precision=4, scheme=Scheme.fixed)),
                    dict(id='ENG2_OIL', name='ENG2 Oil (Qt)'),
                    dict(id='ENG2_OIL_QTZ/FH', name='ENG2 Consumption (Qt/Hr)', type='numeric', format=Format(precision=4, scheme=Scheme.fixed))
        ]  
            
    elif triggered_id == "top5-radio":
        if topVal == "top5_del":
            fig = plotDel()
        elif topVal == "top5_rem":
            fig = plotRem()
        else:
            fig = plot5PIREP()
    else:
        if metricsVal == "dr":
            fig = plotFl(switch)
        elif metricsVal == "si":
            fig = plotSI(switch)
        else:
            fig = plotCOTD(switch)
    
    return fig, " ", " ", " ", tbl, columns
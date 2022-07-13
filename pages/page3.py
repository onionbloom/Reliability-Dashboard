from dash import dcc, html, ctx, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from matplotlib.pyplot import figimage

from plots import plotUCL, plotPirepPerAta
from dataframes import get_pirep_df

### LAYOUT
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='ucl-graph', figure=plotUCL(), config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False))
            ],
            width=9
        ),
        dbc.Col([
            html.H5('Plot Configurations', className="fw-bold text-center", style={"color": "#013764"}),
            dbc.Card([
                dbc.CardBody([
                    dbc.Label("Select Top 5"),
                    dbc.RadioItems(
                        id="pirep-top5-radio",
                        options=[
                            {"label": ata, "value": ata} for ata in get_pirep_df(top5=True).index
                        ],
                        value= get_pirep_df(top5=True).index[0]
                    )
                ])
            ])
        ],
        width=3)
    ], class_name="pt-3"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pirep-ata-graph', config=dict(toImageButtonOptions=dict(width=1871, height=437, filename="dash_graph", format="png"), displaylogo=False))
        ])
    ])
], fluid=True)

### CALLBACKS
@callback(
    Output('pirep-ata-graph','figure'),
    Input('pirep-top5-radio', 'value')
)
def update_graph(ata):
    figure = plotPirepPerAta(ata)

    return figure
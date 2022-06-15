from dash import html, dcc
import dash_bootstrap_components as dbc

from calculations import get_dr, get_FHFC_tot, get_tia, get_del, get_status

cardTitleClasses="card-title text-light text-center fw-bold"

# The dispatch reliability card. Dispatch reliability is calculated with the calc_dr function.
dr = get_dr()
card_dr = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P("Dispatch Reliability", className=cardTitleClasses),
                html.P(
                    "{dr:.2f} %".format(dr=dr),
                    className="card-text fs-2 text-light my-auto text-center", 
                    style={"text-align": "right"},
                )
            ]
        ),
    ],
    color="primary" if dr>=99.80 else "secondary",
    class_name="w-100"
)

# The fleet status card
card_fleet = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H6("Fleet Overview", className="card-title text-light text-center"),
                dbc.Row([
                    dbc.Col([
                        html.P("Aircrafts in fleet",
                            className="card-text text-light"
                        )
                    ]),
                    dbc.Col([
                        html.P("2",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ])
                ],
                justify="between"
                ),
                dbc.Row([
                    dbc.Col([
                        html.P("Aircrafts Operational",
                            className="card-text text-light"
                        )
                    ],
                    width=9
                    ),
                    dbc.Col([
                        html.P("1",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ],
                    width=3
                    )
                ],
                justify="between"
                ),
                dbc.Row([
                    dbc.Col([
                        html.P("AOG",
                            className="card-text text-light"
                        )
                    ]),
                    dbc.Col([
                        html.P("0",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ])
                ],
                justify="between"
                )
            ]
        ),
    ],
    style={"width": "18rem"},
    color="info",
    class_name="w-100"
)

# The maintenance card
card_mtc = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("In Maintenance", className="card-title text-light"),
                dbc.Row([
                    dbc.Col([
                        html.P("Parking / Storage",
                            className="card-text text-light"
                        )
                    ], width=9),
                    dbc.Col([
                        html.P("1",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ], width=3)
                ],
                justify="between"
                ),
                dbc.Row([
                    dbc.Col([
                        html.P("C-check",
                            className="card-text text-light"
                        )
                    ],
                    width=9
                    ),
                    dbc.Col([
                        html.P("0",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ],
                    width=3
                    )
                ],
                justify="between"
                ),
                dbc.Row([
                    dbc.Col([
                        html.P("On Stand-by",
                            className="card-text text-light"
                        )
                    ]),
                    dbc.Col([
                        html.P("0",
                            className="card-text text-light",
                            style={"text-align": "right"}
                        )
                    ])
                ],
                justify="between"
                )
            ]
        ),
    ],
    style={"width": "18rem"},
    color="info",
    class_name="w-100"
)

FH, FC = get_FHFC_tot()
card_FC = dbc.Card(
    [
        dbc.CardBody(
            [
                html.P("Fleet Flight Cycles", className=cardTitleClasses),
                html.P(
                    "{FC:.0f} FC".format(FC=FC),
                    className="card-text fs-2 my-auto text-light text-center"
                )
            ]
        ),
    ],
    color="info",
    class_name="w-100"
)

card_FH = dbc.Card([
    dbc.CardBody([
        html.P("Fleet Flight Hours", className=cardTitleClasses),
        html.P(
            "{FH:.0f} FH".format(FH=FH), className="card-text fs-2 my-auto text-light text-center"
        )
    ])
], color="info", class_name="w-100")

# The TIA rate
tia_rate = get_tia()
card_tia = dbc.Card(
    [
        dbc.CardBody([
            html.H6("TIA Rate", className=cardTitleClasses),
            html.P(
                "{tia:.2f}".format(tia=tia_rate),
                className="card-text fs-2 text-light text-center"
            )
        ])
    ],
    color="primary",
    class_name="w-100"
)

card_cotd = dbc.Card([
    dbc.CardBody([
        html.P("COTD", className=cardTitleClasses),
        html.P(
            '###',
            className="card-text fs-2 fw-bold text-light text-center"
        )
    ])
], color="info", class_name="w-100")

# The delay and cancelations card
delays = get_del()
card_del = dbc.Card([
    dbc.CardBody([
        html.P("Delays", className=cardTitleClasses),
        html.P(
            delays,
            className="card-text fs-2 text-light text-center"
        )
    ])
], color="info", class_name="w-100")

# The AC status card
card_status =  dbc.Card([
    dbc.CardBody([
        dcc.Dropdown(
            id="status-dropdown",
            options=[
                {"label": "PK-PWA", "value":"PK-PWA"},
                {"label": "PK-PWC", "value":"PK-PWC"},
                {"label": "PK-PWD", "value":"PK-PWD"}
            ]
        ),
        dbc.Row([
            dbc.Col([
                html.P("Model:", className="card-text text-start mb-1"),
                html.P("MSN:", className="card-text text-start mb-1"),
                html.P("Weight Variant:", className="card-text text-start mb-1"),
                html.P("Status:", className="card-text text-start mb-1"),
                html.P("Total Hours:", className="card-text text-start mb-1"),
                html.P("Total Cycles:", className="card-text text-start mb-1")

            ],width=6),
            dbc.Col([
                html.P(id='status-model', className="card-text text-end mb-1"),
                html.P(id='status-msn', className="card-text text-end mb-1"),
                html.P(id='status-wv', className="card-text text-end mb-1"),
                html.P(id='status-status', className="card-text text-end mb-1"),
                html.P(id='status-fh', className="card-text text-end mb-1"),
                html.P(id='status-fc', className="card-text text-end mb-1")
            ], width=6)
            ], class_name="pt-3")
        
    ])
])
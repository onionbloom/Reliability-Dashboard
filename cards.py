from dash import html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

from calculations import get_dr_ytd, get_FHFC_tot, get_tia, get_del, get_cotd_ytd

cardTitleClasses="card-title text-light text-center fw-bold"

# The dispatch reliability card. Dispatch reliability is calculated with the calc_dr function.
dr = get_dr_ytd()
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
    color="primary" if dr>=95.00 else "secondary",
    class_name="w-100",
    id="card-dr"
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

# The TIA rate card
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

# The COTD rate card
cotd = get_cotd_ytd()
card_cotd = dbc.Card([
    dbc.CardBody([
        html.P("COTD", className=cardTitleClasses),
        html.P(
            "{cotd:.3f}".format(cotd=cotd),
            className="card-text fs-2 text-light text-center"
        )
    ])
], color="primary" if cotd < 0.2 else "secondary", class_name="w-100", id="card-cotd")

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
], color="info", class_name="w-100", id="card-del")

# The AC status card
status = pd.read_csv("./csv_data_files/CONFIG_DB.csv")[['REGISTRATION', 'STATUS']]
card_status =  dbc.Card([
    dbc.CardBody([
        dash_table.DataTable(
            status.to_dict("records"),
            [{"name": i, "id": i} for i in status.columns],
            style_cell={
                'font-family': 'Segoe UI,-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif',
                'font-size': '0.75rem',
                'text-align': 'center',
            },
            style_header={
                'font-weight':'bold'
            }
        )                
    ])
])
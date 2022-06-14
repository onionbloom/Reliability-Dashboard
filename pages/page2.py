from dash import html, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd


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

### LAYOUT
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("AD/SB Management", className="fw-bold text-center", style={"color": "#2F3B47"}),
            dbc.Card([
                dbc.CardBody([ad_table])
            ])
        ],width=3)
    ])
])

### CALLBACKS
@callback(
    Output('paginated-table','data'),
    Input('paginated-table', "page_current"),
    Input('paginated-table', "page_size")
)
def update_table(page_current, page_size):
    return dff.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')
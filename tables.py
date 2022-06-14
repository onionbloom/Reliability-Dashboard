import pandas as pd
import numpy as np
from dash import dash_table

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
    page_action='custom'
    )
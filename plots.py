from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash_bootstrap_templates import load_figure_template

template = load_figure_template("minty")

def get_x_range(period):

    if period == 'W':
        x0 = datetime.now() - relativedelta(days=+60) 
        x1 = datetime.now() + relativedelta(days=+6)
    elif period == 'M':
        x0 = datetime.now() - relativedelta(months=+3) 
        x1 = datetime.now() + relativedelta(months=+3)

    x_range = [x0.strftime("%Y-%m-%d"), x1.strftime("%Y-%m-%d")]

    return x_range

# Plots the monthly FC utilization summary
def plotFl(weekly):
    # Read csv
    util_raw = pd.read_csv("./csv_data_files/UTIL.csv")
    util_raw['TO_DATETIME'] = pd.to_datetime(util_raw['TO_DATE'] + ' ' + util_raw['TO_TIME (UTC)'])
    util_raw['LAND_DATETIME'] = pd.to_datetime(util_raw['LAND_DATE'] + ' ' + util_raw['LAND_TIME (UTC)'])
    util_raw['FL_DURR'] = util_raw['LAND_DATETIME'] - util_raw['TO_DATETIME']
    util_raw.drop(columns=['TO_DATE', 'TO_TIME (UTC)', 'LAND_DATE', 'LAND_TIME (UTC)'], inplace=True)
    
    if weekly:
        # Create dataframe for weekly DR
        df = util_raw.groupby(pd.Grouper(key='TO_DATETIME', freq='W-WED'))[['CYC', 'DELAY', 'IMPACT_DEL']].sum()
        df['DR'] = (df['CYC'] - df['DELAY']) * 100 / df['CYC']

        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        dr_target = [95.00, 95.00]

        fig2 = px.line(df, x=df.index, y="DR", template=template, line_shape='spline', markers=True)
        fig2.add_trace(go.Scatter(x=["2020-05-01", "2030-05-01"], y=dr_target, name="DR Target", line=dict(color='#F3969A',dash='dash', width=1)))
        fig2.update_traces(
            yaxis='y2',
            hovertemplate='Up to: %{x} <br>Dispatch Reliability: %{y}'
            )

        fig = px.bar(df, x=df.index, y="CYC", template=template)
        fig.update_traces(
            hovertemplate='Up to: %{x} <br>Revenue Flights: %{y}',
            marker_line_width=0,
            width= 86400000 * 6,
            marker_color="#6CC3D4"
            )

        subfig.add_traces(fig.data + fig2.data)
        subfig.update_layout(
            title_text= "Weekly Dispatch Reliability and Utilization",
            title_xanchor="center",
            title_x=0.5,
            xaxis= dict(
                title= "Month",
                type= "date",
                dtick= "M1", 
                range=get_x_range('W'), 
                ticklabelmode="period", 
                ticks="outside",
                ticklen=10,
                minor= dict(
                    ticklen=4,
                    dtick= 1000 * 60 * 60 * 24 * 7,
                )),
            yaxis= dict(title='Number of Flights', tick0=0, dtick=5, tickmode= 'linear', rangemode='tozero', range=[0, 20]),
            yaxis2= dict(title= 'Dispatch Reliability', tick0=85, dtick=5, range=[85, 105], tickmode='linear'),
            modebar= dict(orientation='v', remove=['zoom', 'lasso' , 'autoscale']),
            title_yanchor="top",
            title_y=0.95,
            hovermode='x unified'
        )
    else:
        # Create dataframe for Monthly DR
        df = util_raw.groupby(pd.Grouper(key='TO_DATETIME', freq='M'))[['CYC', 'DELAY', 'IMPACT_DEL']].sum()
        df['DR'] = (df['CYC'] - df['DELAY']) * 100 / df['CYC']

        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        dr_target = [95.00, 95.00]

        fig2 = px.line(df, x=df.index, y="DR", template=template, line_shape='spline', markers=True)
        fig2.add_trace(go.Scatter(x=["2020-05-01", "2030-05-01"], y=dr_target, name="DR Target", line=dict(color='#F3969A',dash='dash', width=1)))
        fig2.update_traces(
            yaxis='y2',
            hovertemplate='Period: %{x} <br>Dispatch Reliability: %{y}'
            )

        fig = px.bar(df, x=df.index, y="CYC", template=template)
        fig.update_traces(
            hovertemplate='Period: %{x} <br>Revenue Flights: %{y}',
            marker_line_width=0,
            width= 86400000*20,
            marker_color="#6CC3D4"
            )

        subfig.add_traces(fig.data + fig2.data)
        subfig.update_layout(
            title_text= "Monthly Dispatch Reliability and Utilization",
            title_xanchor="center",
            title_x=0.5,
            xaxis= dict(
                title='Month', 
                type='date',
                tick0="2022-01-30", 
                dtick='M1',
                ticks="outside",
                ticklen=10, 
                range=get_x_range('M'),
                tickformat="%b \n%Y"),
            yaxis= dict(title='Number of Flights', tick0=20, dtick=5, tickmode= 'linear', rangemode='tozero', range=[20, 50]),
            yaxis2= dict(title= 'Dispatch Reliability', tick0=95, dtick=2, range=[94, 101], tickmode='linear'),
            modebar= dict(orientation='v', remove=['zoom', 'lasso' , 'autoscale']),
            title_yanchor="top",
            title_y=0.95,
            hovermode='x unified'
        )
        
    return subfig

# Plots the top 5 unscheduled removals
def plotRem():
    """
    Function that returns the plot figure for top 5 unscheduled removals
    """

    # Read csv
    rem_raw = pd.read_csv("./csv_data_files/UNSCHED_REM.csv", low_memory=False)
    rem_raw['REM_DATE'] = pd.to_datetime(rem_raw['REM_DATE'], format="%m/%d/%Y")

    # Count the removals for each ATA, sort, and get the top 5
    count = rem_raw.groupby('ATA')['PN'].count()
    df = count.sort_values(ascending=False).head(5)

    fig = px.bar(df, x= df.index, y= df.values, template= template)
    fig.update_layout(
        title_text="Top 5 Removals by ATA Chapter",
        title_x=0.5,
        title_xanchor="center",
        xaxis= dict(title='ATA Chapter', dtick=1),
        yaxis= dict(title='Number of Removals', tick0=0, dtick=5, rangemode='tozero', range=[0, 10]),
        modebar=dict(orientation='v', remove=['zoom', 'lasso', 'autoscale'])
    )
    fig.update_traces(hovertemplate='ATA Chapter: %{x} <br>Removals: %{y}')

    return fig

# Plots the fluids consumption
def plotOil():

    fluids_raw = pd.read_csv("./csv_data_files/FLUIDS.csv")
    fluids = fluids_raw[['AC_REG', 'DATE', 'ENG1_OIL', 'ENG2_OIL']].dropna(thresh=1).set_index('AC_REG')

    fig = px.line(fluids.loc['PK-PWC'], x="DATE", y=["ENG1_OIL", "ENG2_OIL"], line_shape='spline', markers=True)
    newVar = {'ENG1_OIL': 'ENG1', 'ENG2_OIL': 'ENG2'}
    fig.for_each_trace(lambda x: x.update(
        name = newVar[x.name],
        legendgroup = newVar[x.name],
        hovertemplate = x.hovertemplate.replace(x.name, newVar[x.name])
    ))
    fig.update_traces(hovertemplate='Date: %{x}<br>Quantity: %{y} Quarts')
    fig.update_layout(
        title_text= "Engine Oil Consumption",
        title_xanchor="center",
        title_x=0.5,
        xaxis= dict(title='Date', type='date'),
        yaxis= dict(title='Oil in quarts', tick0=0, dtick=1, tickmode='linear', range=[0, 10]),
        modebar= dict(orientation='v', remove=['zoom', 'lasso', 'autoscale']),
        hovermode= 'x unified'
    )

    return fig

# Plot the top5 delays by ATA
def plotDel():

    del_raw = pd.read_csv("./csv_data_files/DELAYS.csv")
    del_raw['DATE'] = pd.to_datetime(del_raw['DATE'], format="%Y-%m-%d")
    df = del_raw[del_raw['INC_TYPE'] == "DELAY"].groupby(by='ATA')['FLT_NUM'].count().sort_values(ascending=False).head(5)

    fig = px.bar(df, x=df.index, y=df.values, template=template)
    fig.update_layout(
        title_text="Top 5 Removals by ATA Chapter",
        title_x=0.5,
        title_xanchor="center",
        xaxis= dict(title='ATA Chapter', dtick=1),
        yaxis= dict(title='Number of Delays', tick0=0, dtick=5, rangemode='tozero', range=[0, 10]),
        modebar=dict(orientation='v', remove=['zoom', 'lasso', 'autoscale'])
    )
    fig.update_traces(hovertemplate='ATA Chapter: %{x} <br>Delays: %{y}')

    return fig

# Plot DR and SI
def plotSI(weekly=False):
    # Read csv
    dr_raw = pd.read_csv("./csv_data_files/DR.csv")
    dr_raw['MON-YEAR'] = pd.to_datetime(dr_raw['MON-YEAR'])

    # Create dataframes
    df = dr_raw

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    dr_target = [99.80, 99.80]

    fig2 = px.line(df, x="MON-YEAR", y="DR", template=template, line_shape='spline', markers=True)
    fig2.add_trace(go.Scatter(x=["2020-05-01", "2030-05-01"], y=dr_target, name="DR Target", line=dict(color='#F3969A',dash='dash', width=1)))
    fig2.update_traces(
        yaxis='y2',
        hovertemplate='Period: %{x} <br>Dispatch Reliability: %{y}'
        )

    fig = px.line(df, x="MON-YEAR", y="SI", template=template, line_shape='spline', markers=True)
    fig.update_traces(
        line_color="#FFCE67",
        hovertemplate='Period: %{x} <br>Severity Index: %{y}'
    )

    subfig.add_traces(fig.data + fig2.data)
    subfig.update_layout(
        title_text= "Monthly Dispatch Reliability and Severity Index",
        title_xanchor="center",
        title_x=0.5,
        xaxis= dict(title='Month', type='date', dtick='M2', range=get_x_range('M')),
        yaxis= dict(title='Severity Index', tick0=0, dtick=1, tickmode= 'linear', rangemode='tozero', range=[0, 10]),
        yaxis2= dict(title= 'Dispatch Reliability', tick0=92, dtick=2, range=[92, 102], tickmode='linear'),
        modebar= dict(orientation='v', remove=['zoom', 'lasso' , 'autoscale']),
        title_yanchor="top",
        title_y=0.95,
        hovermode='x unified'
    )

    return subfig

# Plot DR and COTD
def plotCOTD(weekly):
    util_raw = pd.read_csv("./csv_data_files/UTIL.csv")
    util_raw['TO_DATETIME'] = pd.to_datetime(util_raw['TO_DATE'] + ' ' + util_raw['TO_TIME (UTC)'])
    util_raw['LAND_DATETIME'] = pd.to_datetime(util_raw['LAND_DATE'] + ' ' + util_raw['LAND_TIME (UTC)'])
    util_raw['FL_DURR'] = util_raw['LAND_DATETIME'] - util_raw['TO_DATETIME']
    util_raw.drop(columns=['TO_DATE', 'TO_TIME (UTC)', 'LAND_DATE', 'LAND_TIME (UTC)'], inplace=True)

    if weekly:
        # Create dataframe for weekly DR
        df = util_raw.groupby(pd.Grouper(key='TO_DATETIME', freq='W-WED'))[['CYC', 'DELAY', 'IMPACT_DEL']].sum()
        df['DR'] = (df['CYC'] - df['DELAY']) * 100 / df['CYC']
        df['COTD'] = (df['DELAY'] + df['IMPACT_DEL']) / df['CYC']

        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        dr_target = [95.00, 95.00]

        fig2 = px.line(df, x=df.index, y="DR", template=template, line_shape='spline', markers=True)
        fig2.add_trace(go.Scatter(x=["2020-05-01", "2030-05-01"], y=dr_target, name="DR Target", line=dict(color='#F3969A',dash='dash', width=1)))
        fig2.update_traces(
            yaxis='y2',
            hovertemplate='Period: %{x} <br>Dispatch Reliability: %{y}'
            )

        fig = px.line(df, x=df.index, y="COTD", template=template, line_shape='spline', markers=True)
        fig.update_traces(
            hovertemplate='Up to: %{x} <br>COTD: %{y}',
            line_color="#FFCE67"
            )

        subfig.add_traces(fig.data + fig2.data)
        subfig.update_layout(
            title_text= "Weekly Reliability and Delay Contribution",
            title_xanchor="center",
            title_x=0.5,
            xaxis= dict(
                title= "Month",
                type= "date",
                dtick= "M1", 
                range=get_x_range('W'),
                ticklabelmode="period",
                ticks="outside",
                ticklen=10,
                minor= dict(
                    ticklen=4,
                    dtick= 1000 * 60 * 60 * 24 * 7,
                )),
            yaxis= dict(title='COTD', tick0=0, dtick=0.1, tickmode= 'linear', rangemode='tozero', range=[0, 1]),
            yaxis2= dict(title= 'Dispatch Reliability', tick0=85, dtick=5, range=[75, 105], tickmode='linear'),
            modebar= dict(orientation='v', remove=['zoom', 'lasso' , 'autoscale']),
            title_yanchor="top",
            title_y=0.95,
            hovermode='x unified'
        )
    else:
        # Create dataframe for Monthly DR
        df = util_raw.groupby(pd.Grouper(key='TO_DATETIME', freq='M'))[['CYC', 'DELAY', 'IMPACT_DEL']].sum()
        df['DR'] = (df['CYC'] - df['DELAY']) * 100 / df['CYC']
        df['COTD'] = (df['DELAY'] + df['IMPACT_DEL']) / df['CYC']

        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        dr_target = [95.00, 95.00]

        fig2 = px.line(df, x=df.index, y="DR", template=template, line_shape='spline', markers=True)
        fig2.add_trace(go.Scatter(x=["2020-05-01", "2030-05-01"], y=dr_target, name="DR Target", line=dict(color='#F3969A',dash='dash', width=1)))
        fig2.update_traces(
            yaxis='y2',
            hovertemplate='Period: %{x} <br>Dispatch Reliability: %{y}'
            )

        fig = px.line(df, x=df.index, y="COTD", template=template, line_shape='spline', markers=True)
        fig.update_traces(
            hovertemplate='Period: %{x} <br>COTD: %{y}',
            line_color="#FFCE67"
            )

        subfig.add_traces(fig.data + fig2.data)
        subfig.update_layout(
            title_text= "Monthly Dispatch Reliability and Delay Contribution",
            title_xanchor="center",
            title_x=0.5,
            xaxis= dict(
                title='Month', 
                type='date',
                tick0="2022-01-30", 
                dtick='M1',
                ticks="outside",
                ticklen=10, 
                range=get_x_range('M'),
                tickformat="%b \n%Y"),
            yaxis= dict(title='COTD', tick0=0, dtick=0.1, tickmode= 'linear', rangemode='tozero', range=[0, 1]),
            yaxis2= dict(title= 'Dispatch Reliability', tick0=95, dtick=2, range=[94, 101], tickmode='linear'),
            modebar= dict(orientation='v', remove=['zoom', 'lasso' , 'autoscale']),
            title_yanchor="top",
            title_y=0.95,
            hovermode='x unified'
        )
    
    return subfig
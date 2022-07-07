import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from dataframes import get_util_df

def get_dr(month=datetime.now().month-1, year=datetime.now().year):
    """
    Function to calculate the dispatch reliability for a given month and year. The parameter inputs are:
    month: The month that the DR is to be calculated for (eg. MM)
    """

    dr_raw = pd.read_csv("./csv_data_files/DR.csv")
    dr_raw['MON-YEAR'] = pd.to_datetime(dr_raw['MON-YEAR'])

    # Filter the dataframe to the month and year specified
    filtered_df = (dr_raw['MON-YEAR'].dt.month == month) & (dr_raw['MON-YEAR'].dt.year == year)

    # Calculated dispatch reliability
    DR = dr_raw[filtered_df]['DR'].item()

    return DR

def get_dr_ytd():
    """
    Function to get the YTD dispatch reliability
    """
    util_df = get_util_df()
    # Filter year-to-date
    last12Month = datetime.now() - relativedelta(months=+12)
    df_ytd = util_df[util_df['TO_DATETIME'] > last12Month]

    # Calculate YTD DR
    DR_YTD = (df_ytd['CYC'].sum() - df_ytd['DELAY'].sum()) * 100 / df_ytd['CYC'].sum()

    return DR_YTD

def get_cotd_ytd():
    """
    Function to get the YTD contribution of technical delays
    """
    util_df = get_util_df()
    # Filter year-to-date
    last12Month = datetime.now() - relativedelta(months=+12)
    df_ytd = util_df[util_df['TO_DATETIME'] > last12Month]

    # Calculate the YTD COTD
    COTD_YTD = (util_df['IMPACT_DEL'].sum() + util_df['DELAY'].sum()) / util_df['CYC'].sum()

    return COTD_YTD




def get_FHFC_tot():
    """
    Function to calculate the total fleet hours (FH) and total fleet cycles (FC). No input parameters is required.
    """
    util_df = get_util_df()
    FH = util_df['FL_DURR'].sum()/np.timedelta64(1,'s')/3600
    FC = util_df['CYC'].sum()

    return FH, FC
    
def get_tia(month=datetime.now().month-1, year=datetime.now().year):
    """
    Function that gets the TIA Rate from db
    """

    dr_raw = pd.read_csv("./csv_data_files/DR.csv")
    dr_raw['MON-YEAR'] = pd.to_datetime(dr_raw['MON-YEAR'])
    
    # Get the TIA Rate
    filtered_df = (dr_raw['MON-YEAR'].dt.month == month) & (dr_raw['MON-YEAR'].dt.year == year)
    tia = dr_raw[filtered_df]['TIA_RATE'].item()

    return tia

def get_del():
    """
    Function that gets the total number of delays
    """
    util_df = get_util_df()
    delays = util_df['DELAY'].sum() + util_df['IMPACT_DEL'].sum()

    return delays

def get_status():
    """
    Function that gets the status of each aircraft registration
    """
    status = pd.read_csv("./csv_data_files/CONFIG_DB.csv")[['MSN', 'REGISTRATION', 'AIRCRAFT TYPE', 'CURR_TOTAL_HOURS', 'CURR_TOTAL_CYCLES', 'STATUS', 'WEIGHT VARIANT']]

    return status
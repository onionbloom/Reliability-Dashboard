import pandas as pd
import numpy as np
from datetime import datetime

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

def get_FHFC_tot():
    """
    Function to calculate the total fleet hours (FH) and total fleet cycles (FC). No input parameters is required.
    """

    raw_csv = pd.read_csv("./csv_data_files/CONFIG_DB.csv")

    raw_csv['EIS TOTAL HOURS'] = (pd.to_timedelta(raw_csv['EIS TOTAL HOURS'])/np.timedelta64(1,'s'))/3600
    eis_hours = raw_csv['EIS TOTAL HOURS'].sum().astype('int32')
    fleet_hours = raw_csv['CURR_TOTAL_HOURS'].sum().astype('int32')
    FH = fleet_hours - eis_hours
    FC = int(raw_csv['CURR_TOTAL_CYCLES'].sum()) - raw_csv['EIS TOTAL CYCLES'].sum().astype('int32')

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

def get_del(month=datetime.now().month-1, year=datetime.now().year):
    """
    Function that gets the number of delays
    """

    del_raw = pd.read_csv("./csv_data_files/DELAYS.csv")
    del_raw['DATE'] = pd.to_datetime(del_raw['DATE'], format="%Y-%m-%d")

    delays = del_raw[(del_raw['DATE'].dt.month == month) & (del_raw['DATE'].dt.year == year)].count('rows')[1]

    return delays

def get_status():
    """
    Function that gets the status of each aircraft registration
    """
    status = pd.read_csv("./csv_data_files/CONFIG_DB.csv")[['MSN', 'REGISTRATION', 'AIRCRAFT TYPE', 'CURR_TOTAL_HOURS', 'CURR_TOTAL_CYCLES', 'STATUS', 'WEIGHT VARIANT']]

    return status
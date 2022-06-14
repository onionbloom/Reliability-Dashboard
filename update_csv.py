import pandas as pd
from datetime import datetime
import numpy as np

util_raw = pd.read_csv("./csv_data_files/UTIL.csv")
util_raw['TO_DATETIME'] = pd.to_datetime(util_raw['TO_DATE'] + ' ' + util_raw['TO_TIME (UTC)'])
util_raw['LAND_DATETIME'] = pd.to_datetime(util_raw['LAND_DATE'] + ' ' + util_raw['LAND_TIME (UTC)'])
util_raw['FLT_DURR'] = util_raw['LAND_DATETIME'] - util_raw['TO_DATETIME']
util_raw.drop(columns=['TO_DATE', 'TO_TIME (UTC)', 'LAND_DATE', 'LAND_TIME (UTC)'], inplace=True)

# Update the config db
def updateConf():
    config_raw = pd.read_csv("./csv_data_files/AC_CONFIG_CATALOG.csv",)
    config_raw['EIS TOTAL HOURS'] = config_raw['EIS TOTAL HOURS'] + ':00'
    config_raw['EIS TOTAL HOURS'] = pd.to_timedelta(config_raw['EIS TOTAL HOURS'])

    curr_hours = [ ((config_raw[config_raw['REGISTRATION'] == reg]['EIS TOTAL HOURS'].item() + util_raw[util_raw['AC_REG'] == reg]['FLT_DURR'].sum())/np.timedelta64(1,'s'))/3600 for reg in config_raw['REGISTRATION']]
    curr_cycles = [ config_raw[config_raw['REGISTRATION'] == reg]['EIS TOTAL CYCLES'].item() + util_raw[util_raw['AC_REG'] == reg]['CYC'].sum() for reg in config_raw['REGISTRATION']]

    config_raw['CURR_TOTAL_HOURS'] = curr_hours
    config_raw['CURR_TOTAL_CYCLES'] = curr_cycles

    config_raw.to_csv("./csv_data_files/CONFIG_DB.csv", index=False)

# Update the DR db
def updateDR(month=datetime.now().month-1, year=datetime.now().year):
    del_raw = pd.read_csv("./csv_data_files/DELAYS.csv")
    del_raw['DATE'] = pd.to_datetime(del_raw['DATE'])

    summation = del_raw[(del_raw['DATE'].dt.month == month) & (del_raw['DATE'].dt.year == year)].groupby('INC_TYPE')['WEIGHT'].sum().sum()

    mon_rev_fl = util_raw.groupby(util_raw['TO_DATETIME'].dt.month == month)['CYC'].sum()[1]

    SI = (100*summation)/mon_rev_fl

    t_delta = util_raw.groupby(util_raw['TO_DATETIME'].dt.month == month)['FLT_DURR'].sum()[1]
    mon_fleet_hours = (t_delta/np.timedelta64(1,'s'))/3600

    mon_num_del = len(del_raw[del_raw['DATE'].dt.month == month])

    DR = int(((mon_rev_fl-mon_num_del)/mon_rev_fl)*100)  

    dr_raw = pd.read_csv("./csv_data_files/DR.csv")
    dr_raw['MON-YEAR'] = pd.to_datetime(dr_raw['MON-YEAR'])

         
    mon_year_filter = (dr_raw['MON-YEAR'].dt.month == month) & (dr_raw['MON-YEAR'].dt.year == year)
    tia = dr_raw[mon_year_filter]['TIA'].item()
    tia_rate = (tia/mon_fleet_hours)*1000
    dr_raw[mon_year_filter] = [datetime(year, month, 1), mon_rev_fl, mon_num_del, mon_fleet_hours, mon_rev_fl, DR, tia, tia_rate, SI]

    dr_raw.to_csv("./csv_data_files/DR.csv", index=False)

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

# Update the LLP util
def updateLLP():
    llp_raw  = pd.read_csv("./csv_data_files/LLP_UTIL.csv")
    llp_raw['INSTALL_DATE'] = pd.to_datetime(llp_raw['INSTALL_DATE'], format="%Y-%m-%d")

    # Update the current TSNs
    compile_curr=[]
    for reg in llp_raw['REG'].unique():
        curr_tsn = llp_raw[llp_raw['REG'] == reg]['EIS_TSN'] + round(util_raw[util_raw['AC_REG'] == reg]['FLT_DURR'].sum()/np.timedelta64(1,'s')/3600,1)
        compile_curr.extend(curr_tsn)
    llp_raw['CURR_TSN'] = compile_curr

    # Update the current CSNs
    compile_curr=[]
    for reg in llp_raw['REG'].unique():
        curr_csn = llp_raw[llp_raw['REG'] == reg]['EIS_CSN'] + util_raw[util_raw['AC_REG'] == reg]['CYC'].sum()
        compile_curr.extend(curr_csn)
    llp_raw['CURR_CSN'] = compile_curr

    # Update TSI, CSI
    llp_raw['TSI'] = llp_raw['CURR_TSN'] - llp_raw['INSTALL_TSN']
    llp_raw['CSI'] = llp_raw['CURR_CSN'] - llp_raw['INSTALL_CSN']

    # Update TLSV, CLSV
    llp_raw['TLSV'] = llp_raw['CURR_TSN'] - llp_raw['SV_TSN']
    llp_raw['CLSV'] = llp_raw['CURR_CSN'] - llp_raw['SV_CSN']

    # Update days since installation
    llp_raw['DAYS_SINCE_INSTALL'] = datetime.now() - llp_raw['INSTALL_DATE']

    # Update Hrs per Day, Cycs per Day
    llp_raw['HRS_PER_DAY'] = llp_raw['TSI'] / llp_raw['DAYS_SINCE_INSTALL'].dt.days
    llp_raw['CYCLES_PER_DAY'] = llp_raw['CSI'] / llp_raw['DAYS_SINCE_INSTALL'].dt.days

    # Write into csv
    llp_raw.to_csv("./csv_data_files/LLP_UTIL.csv", index=False)

def updateENG_LLP(SNR):
    """
    Function that updates the Engine LLP Status 
    """
    llp_raw = pd.read_csv('./csv_data_files/LLP_UTIL.csv')
    llp_raw['INSTALL_DATE'] = pd.to_datetime(llp_raw['INSTALL_DATE'], format="%Y-%m-%d")

    eng_raw = pd.read_csv("./csv_data_files/{SNR}.csv".format(SNR=SNR))

    TLSV = llp_raw[llp_raw['SNR'] == SNR]['TLSV'].item()
    CLSV = llp_raw[llp_raw['SNR'] == SNR]['CLSV'].item()
    CYC_P_DAY = llp_raw[llp_raw['SNR'] == SNR]['CYCLES_PER_DAY'].item()

    eng_raw['LLP_TSN'] = eng_raw['LLP_HRS_AT_SV'] + TLSV
    eng_raw['LLP_CSN'] = eng_raw['LLP_CYC_AT_SV'] + CLSV
    eng_raw['%_CYC_USED'] = round(((eng_raw['CYC_LIMIT'] - eng_raw['LLP_CSN']) / eng_raw['CYC_LIMIT']) * 100, 2)
    eng_raw['%_CYC_REM'] = 100 - eng_raw['%_CYC_USED']
    eng_raw['REM_CYC'] = eng_raw['CYC_LIMIT'] - eng_raw['LLP_CSN']
    eng_raw['LLP_DUE'] = datetime.now() + pd.to_timedelta(eng_raw['REM_CYC']/CYC_P_DAY, unit='D')
    eng_raw['LLP_DUE'] = eng_raw['LLP_DUE'].dt.date

    # Write into csv
    eng_raw.to_csv("./csv_data_files/{SNR}.csv".format(SNR=SNR), index=False)


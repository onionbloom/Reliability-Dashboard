import pandas as pd


util_df = pd.read_csv("./csv_data_files/UTIL.csv")
util_df['TO_DATETIME'] = pd.to_datetime(util_df['TO_DATE'] + ' ' + util_df['TO_TIME (UTC)'])
util_df['LAND_DATETIME'] = pd.to_datetime(util_df['LAND_DATE'] + ' ' + util_df['LAND_TIME (UTC)'])
util_df['FL_DURR'] = util_df['LAND_DATETIME'] - util_df['TO_DATETIME']
util_df.drop(columns=['TO_DATE', 'TO_TIME (UTC)', 'LAND_DATE', 'LAND_TIME (UTC)'], inplace=True)


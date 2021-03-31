import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

api_key = '4VU02OKEYKOXMVHL'
ts = TimeSeries(key=api_key, output_format='csv')
totalData = ts.get_intraday_extended(symbol='MSFT',slice="year1month1", interval = '1min')
dd = totalData
#csv --> dataframe
df = pd.DataFrame(list(dd[0]))

#setup of column and index
header_row=0
df.columns = df.iloc[header_row]
df = df.drop(header_row)
df.set_index('time', inplace=True)

#show output
print(df)

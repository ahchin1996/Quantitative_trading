import numpy
import talib
import pandas_datareader as pdr
import pandas as pd

# 看一下全部的函數，https://mrjbq7.github.io/ta-lib/funcs.html
all_functions = talib.get_functions()
print(len(all_functions))
print(all_functions)

SPY = pdr.get_data_tiingo('SPY', api_key='63e3bed28936dbb6416aeb18440310f60884fcf6')
SPY = SPY.reset_index(level=[0,1])

SPY.index = SPY['date']
SPY_adj = SPY.iloc[:,7:12]
SPY_adj.columns = ['Close','High','Low','Open','Volume']
Close = SPY_adj.Close
Close2019 = Close['2019']
SPY2019 = SPY_adj["2019"]

roc = talib.ROC(Close2019,1).values

roc = pd.Series(index=SPY2019.index,data= roc)

SPY2019.drop("ROC",axis = 1)
SPY2019.insert(len(SPY2019.columns),"ROC",roc)
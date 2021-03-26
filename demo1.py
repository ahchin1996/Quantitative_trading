import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import pandas_datareader as pdr
import datetime

cerebro = bt.Cerebro()

#First
# GSPC = btfeeds.YahooFinanceData(dataname='^GSPC',
#                                 fromdate=datetime.datetime(2019, 1, 1),
#                                 todate=datetime.datetime(2019, 12, 31))

#Second
brf_daily = btfeeds.GenericCSVData(
    dataname='new_data/^GSPC.csv',
    fromdate=datetime.datetime(2019, 1, 1),
    todate=datetime.datetime(2019, 12, 31),
    nullvalue=0.0,
    dtformat=('%Y-%m-%d'),
    datetime=0,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=5,
    openinterest=-1
)

#Third
# start = datetime.datetime(2020, 1, 2)
# end = datetime.datetime(2020, 12, 31)
# TWII = pdr.data.DataReader("^TWII", 'yahoo', start, end)
# data = btfeeds.PandasData(dataname=TWII)

class MyStrategy(bt.Strategy):
    pass

cerebro.adddata(brf_daily)

cerebro.addstrategy(MyStrategy)

cerebro.run()

cerebro.plot(style = "candle")
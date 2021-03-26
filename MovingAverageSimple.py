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
    fromdate=datetime.datetime(2018, 1, 1),
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
    def __init__(self):
        self.sma = bt.indicators.MovingAverageSimple(self.data,period = 24)
        self.cro_sig = bt.ind.CrossOver(self.data.close,self.sma)

    def start(self):
        print("start")

    def prenext(self):
        print("prenext")

    def nextstart(self):
        print("nextstart")

    def next(self):
        print("A new bar")
        # print(self.data.close[0])
        # ma_value = sum([self.data.close[-cnt] for cnt in range(24)])/24
        # ma_value = self.sma[0]
        # pre_ma_value = self.sma[-1]
        # if self.data.close[0] > ma_value and self.data.close[-1] < pre_ma_value:
        #     self.order = self.buy()
        #     print("long" , self.data.datetime.date())
        # elif self.data.close[0] < ma_value and self.data.close[-1] > pre_ma_value:
        #     self.order = self.sell()
        #     print("short", self.data.datetime.date())
        if not self.position and self.cro_sig[0] == 1:
            self.order = self.buy()
        elif not self.position and self.cro_sig[0] == -1:
            self.order = self.sell()
        elif self.position and self.cro_sig[0] == 1:
            self.order = self.close()
            self.order = self.buy()
        elif self.position and self.cro_sig[0] == -1:
            self.order = self.close()
            self.order = self.sell()

        print(self.cro_sig[0])

    def stop(self):
        print("stop")


cerebro.adddata(brf_daily)

cerebro.addstrategy(MyStrategy)

cerebro.run()

cerebro.plot(style = "candle")
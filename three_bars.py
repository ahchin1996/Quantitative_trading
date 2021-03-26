import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import pandas_datareader as pdr

class three_bars(bt.Indicator):
    lines = ('up','down')
    def __init__(self):
        self.addminperiod(4)
        self.plotinfo.plotmaster = self.data
        self.plotinfo.plot = False


    def next(self):
        self.lines.up[0] = max(max(self.data.close.get(ago = -1,size = 3)),max(self.data.open.get(ago = -1,size = 3)))
        self.lines.down[0] = min(min(self.data.close.get(ago=-1, size=3)), min(self.data.open.get(ago=-1, size=3)))

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.up_down = three_bars(self.data)
        self.buy_sig = bt.indicators.CrossOver(self.data.close,self.up_down.up)
        self.sell_sig = bt.indicators.CrossOver(self.data.close,self.up_down.down)
        self.buy_sig.plotinfo.plot = False
        self.sell_sig.plotinfo.plot = False
        # self.up_down.plotinfo.plot = False

    def next(self):
        if not self.position and self.buy_sig[0] == 1:
            self.order = self.buy()

        if self.getposition().size < 0 and self.buy_sig[0] == 1:
            self.order = self.close()
            self.order = self.buy()

        if not self.position and self.sell_sig[0] == 1:
            self.order = self.sell()

        if self.getposition().size >0 and self.sell_sig[0] == 1:
            self.order = self.close()
            self.order = self.sell()

if __name__ == "__main__":

    cerebro = bt.Cerebro()

    brf_daily = btfeeds.GenericCSVData(
    dataname='D:/Time_Series_Research/new_data/^GSPC.csv',
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

    cerebro.adddata(brf_daily)

    cerebro.addstrategy(MyStrategy)

    cerebro.run()

    cerebro.plot(style = "candle")
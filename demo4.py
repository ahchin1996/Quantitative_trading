import datetime
import backtrader as bt
import pandas as pd
import backtrader.feeds as btfeeds
import pandas_datareader as pdr

class DT_Line(bt.Indicator):
    lines = ('U','D')
    params = (('period',2),('k_u',.7),('k_d',.7))
    def __init__(self):
        self.addminperiod(self.p.period +1)
        self.plotinfo.plotmaster = self.data

    def next(self):
        HH = max(self.data.high.get(-1,size = self.p.period))
        LC = min(self.data.close.get(-1,size = self.p.period))
        HC = max(self.data.close.get(-1,size = self.p.period))
        LL = min(self.data.low.get(-1,size = self.p.period))
        r = max(HH - LC  ,LL - HC)
        self.lines.U[0] = self.data.open[0] + self.p.k_u * r
        self.lines.D[0] = self.data.open[0] - self.p.k_d * r

class DualThrust(bt.Strategy):
    def __init__(self):
        self.dataclose = self.data.close
        self.D_Line = DT_Line(self.data)
        # self.D_Line.plotinfo.plot = False

    def next(self):
        pass

if __name__ == "__main__":

    cerebro = bt.Cerebro()

    TWII = pdr.data.DataReader("^TWII", 'yahoo')

    brf_min_bar = bt.feeds.PandasData(
    dataname= TWII,
    fromdate=datetime.datetime(2018, 1, 1),
    todate=datetime.datetime(2019, 12, 31),
    timeframe=bt.TimeFrame.Days
    )

    cerebro.adddata(brf_min_bar)
    # cerebro.resampledata(brf_min_bar,timeframe = bt.TimeFrame.Days)

    cerebro.addstrategy(DualThrust)

    cerebro.run()

    cerebro.plot(style = "candle")
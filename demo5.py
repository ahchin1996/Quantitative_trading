import datetime
import backtrader as bt
import pandas as pd
import backtrader.feeds as btfeeds
import pandas_datareader as pdr
from tiingo import TiingoClient
import time

class DT_Line(bt.Indicator):
    lines = ('U','D')
    params = (('period',2),('k_u',.7),('k_d',.7))
    def __init__(self):
        self.addminperiod(self.p.period +1)
        # self.plotinfo.plotmaster = self.data

    def next(self):
        HH = max(self.data.high.get(-1,size = self.p.period))
        LC = min(self.data.close.get(-1,size = self.p.period))
        HC = max(self.data.close.get(-1,size = self.p.period))
        LL = min(self.data.low.get(-1,size = self.p.period))
        r = max(HH - LC  ,LL - HC)
        self.lines.U[0] = self.data.open[0] + self.p.k_u * r
        self.lines.D[0] = self.data.open[0] - self.p.k_d * r

class DualThrust(bt.Strategy):
    params = (('period',2),('k_u',.7),("k_d",.7))
    def __init__(self):
        self.dadclose = self.data.close
        self.D_Line = DT_Line(self.data1, period = self.p.period, k_u = self.p.k_u, k_d = self.p.k_d)
        self.D_Line = self.D_Line()
        self.D_Line.plotinfo.plotmaster = self.data0
        self.data1.plotinfo.plot = False

        self.buy_sig = bt.indicators.CrossOver(self.data.close, self.D_Line.U)
        self.sell_sig = bt.indicators.CrossDown(self.data.close, self.D_Line.D)

    def start(self):
        print("the world call me")

    def prenext(self):
        print("not mature")

    def next(self):
        if self.data.datetime.time() > datetime.time(9,3) and self.data.datatime.time < datetime.time(15,30):
            if not self.position and self.buy_sig[0] ==1:
                self.order = self.buy()
            if not self.position and self.sell_sig[0] == 1:
                self.order = self.sell()
            if self.getposition().size < 0 and self.buy_sig[0] == 1:
                self.order = self.close()
                self.order = self.buy()
            if self.getposition().size > 0 and self.sell_sig[0] ==1:
                self.order  = self.close()
                self.order = self.sell()

        if self.data.datetime.time() > datetime.time(15,30) and self.position:
            self.order = self.close()
    def stop(self):
        print('period: %s, k_u: %s, k_d: %s,final_value: %.2f '%
              (self.p.period,self.p.k_u,self.p.k_d,self.broker.getvalue()))

if __name__ == "__main__":

    cerebro = bt.Cerebro()

    TWII = pdr.data.DataReader("^TWII", 'yahoo')

    brf_min_bar = bt.feeds.PandasData(
    dataname= TWII,
    fromdate=datetime.datetime(2019, 5, 1),
    todate=datetime.datetime(2019, 6, 30),
    timeframe=bt.TimeFrame.Minutes
    )

    cerebro.adddata(brf_min_bar)
    cerebro.resampledata(brf_min_bar,timeframe = bt.TimeFrame.Days)

    # cerebro.addstrategy(DualThrust)
    cerebro.optstrategy(
        DualThrust,
        period = range(1,5),
        k_u = [n/100 for  n in range(2,10)],
        k_d = [n/100 for  n in range(2,10)]
    )

    cerebro.run()
    #
    # cerebro.plot(style = "candle")
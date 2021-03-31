import datetime
import backtrader as bt
import pandas as pd
import backtrader.feeds as btfeeds
import pandas_datareader as pdr
from tiingo import TiingoClient
import time


class RSI_Sta(bt.Strategy):
    params = (('period',24),('upper',70),("lower",40))
    def __init__(self):
        self.rsi = bt.ind.RSI(self.data.close,period = self.p.period)
        self.buy_sig = bt.indicators.CrossOver(self.rsi,bt.LineNum(self.p.upper))
        self.sell_sig = bt.indicators.CrossDown(self.rsi,bt.LineNum(self.p.lower))

    def start(self):
        print("the world call me")

    def prenext(self):
        print("not mature")

    def next(self):
        if self.rsi > self.p.upper  and self.position:
            self.sell()
        elif self.rsi < self.p.lower and not self.position:
            self.buy()


    def stop(self):
        print('period: %s, upper: %s, lower: %s,final_value: %.2f '%
              (self.p.period,self.p.upper,self.p.lower,self.broker.getvalue()))

if __name__ == "__main__":

    cerebro = bt.Cerebro()
    data = btfeeds.YahooFinanceData(dataname='AAPL',
                                    fromdate=datetime.datetime(2019, 1, 1),
                                    todate=datetime.datetime(2019, 12, 31))
    cerebro.adddata(data)

    cerebro.addstrategy(RSI_Sta)
    # cerebro.optstrategy(
    #     RSI_Sta,
    #     period = range(6,16),
    #     upper = range(70,91),
    #     lower = range(10,31)
    # )
    #
    cerebro.run()

    cerebro.plot(style = "candle")
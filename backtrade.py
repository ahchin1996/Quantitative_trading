# data feeds
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

# 從Yahoo Finance取得資料
data = btfeeds.YahooFinanceData(dataname='SPY',
                                fromdate=datetime.datetime(2019, 1, 1),
                                todate=datetime.datetime(2019, 12, 31))


# sma cross strategy
class SmaCross(bt.Strategy):
    # 交易紀錄
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # 設定交易參數
    params = dict(
        ma_period_short=5,
        ma_period_long=10
    )

    def __init__(self):
        # 均線交叉策略
        sma1 = bt.ind.SMA(period=self.p.ma_period_short)
        sma2 = bt.ind.SMA(period=self.p.ma_period_long)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

        # 使用自訂的sizer函數，將帳上的錢all-in
        self.setsizer(sizer())

        # 用開盤價做交易
        self.dataopen = self.datas[0].open

from fileinput import close
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from sqlalchemy import column
from database import Database
import config
from data_fetch import DataFetcher
import sqlite3

class simplestrat(Strategy):
    n = 20

    def init(self):
        close = self.data.Close
        self.sma = self.I(talib.SMA, close, self.n)   # I = func from backtest module used to create an indicator. grammar: I(indicator_names, args)

    def next(self):
        price = self.data.Close
        sma = self.sma[-1]
        yesterdays_low = self.data.Low[-2]
        stop_loss = yesterdays_low
        take_profit = yesterdays_low + 1.6 * (price - stop_loss)

        if self.position.is_long:
            if price <= stop_loss or price >= take_profit:
                self.position.close()

        elif price > sma:
            print(stop_loss, ', ', take_profit)
            try:
                self.buy(sl = stop_loss, tp = take_profit)
            except:
                pass


db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
data = pd.read_csv(db)
data.columns = [column.capitalize() for column in data.columns]

bt = Backtest(data, simplestrat, cash=1000000, commission=.002)
stats = bt.run()
print(stats)
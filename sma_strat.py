import numpy as np
import pandas as pd
import talib
from backtesting import Strategy

class SMA_strat(Strategy):
    n = 20
    m = 60

    def init(self):
        close = self.data.Close
        self.sma_short = self.I(talib.SMA, close,self.n)
        self.sma_long = self.I(talib.SMA, close, self.m)

    def next(self):
        price = self.data.Close
        sma_short = self.sma_short
        sma_long = self.sma_long
        stop_loss = 600
        take_profit = 1.6 * (price - stop_loss)


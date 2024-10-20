import numpy as np
import pandas as pd
import talib
from backtesting import Strategy
from backtesting.lib import crossover

class SMA_cross(Strategy):
    s = 20
    l = 60

    def init(self):
        self.short_sma = self.I(talib.SMA, self.data.Close, self.s)
        self.long_sma = self.I(talib.SMA, self.data.Close, self.l)

    def next(self):
        if crossover(self.short_sma, self.long_sma):
            self.position.close()
            self.sell()
        elif crossover(self.long_sma, self.short_sma):
            self.position.close()
            self.buy()
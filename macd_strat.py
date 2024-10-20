import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
from tensorflow.python.data.experimental.ops.testing import sleep
import config
import talib


def macd_indicator(close, n1=12, n2=26, n3=9):
    macd, signal, hist = talib.MACD(close, fastperiod=n1, slowperiod=n2, signalperiod=n3)
    return macd  # or return (macd, signal, hist) based on what you want


class MACD_strat(Strategy):
    n1 = 12
    n2 = 26
    n3 = 9

    def init(self):
        # Correct function call: using I() to integrate the custom indicator
        self.macd = self.I(macd_indicator, self.data.Close, self.n1, self.n2, self.n3)

    def next(self):
        # self.macd is now a series, check for its values
        if crossover(self.macd,0):
            if not self.position:
                self.buy()
            else:
                self.position.close()

        if crossover(0,self.macd):
            if not self.position:
                self.sell()
            else:
                self.position.close()
                self.buy()
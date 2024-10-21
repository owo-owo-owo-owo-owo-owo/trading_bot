import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
import config
import talib

def rsi_indicator(close,time):
    rsi = talib.RSI(close,time)
    return rsi

def sma_indicator(close, time):
    sma = talib.SMA(close,time)
    return sma

class RSI_MA_cross(Strategy):
    RSI_overbought = 60
    RSI_oversold = 40
    time = 10

    def init(self):
        self.rsi = self.I(rsi_indicator,self.data.Close, self.time)
        self.sma = self.I(sma_indicator,self.data.Close, self.time)

    def next(self):
        if self.rsi > self.RSI_overbought and self.data.Close > self.sma:
            if not self.position:
                self.sell(limit=300000)
            elif self.position.is_long:
                self.position.close()
                self.sell(limit=300000)

        elif self.rsi < self.RSI_oversold and self.data.Close < self.sma:
            if not self.position:
                self.buy(limit=300000)
            elif self.position.is_short:
                self.position.close()
                self.buy(limit=300000)
from fileinput import close
import numpy as np
import pandas as pd
from backtesting import Strategy

import config
from config import STRATEGY

from ta.trend import macd


class MACD_strat(Strategy):
    def __init__(self):
        self.db = Database()
        self.data = None

    def macd(self):
        if self.data is None:
            print("No data available for backtesting.")
            return

        df = self.data.copy()
        df['macd'] = macd(df["close"],window_slow=30,window_fast=6,fillna=False)  #calcolo indicatore MACD fatto automaticamente da ta.trend.macd
        df['signal'] = np.where(df['macd'] > 0, 1, -1)
        df['position'] = df['signal'].diff()



        return df
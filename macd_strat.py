from fileinput import close
import numpy as np
import pandas as pd
import config
from database import Database
from ta.trend import macd


class MACD_strat:
    def __init__(self):
        self.db = Database()
        self.data = None

    def macd(self):
        if self.data is None:
            print("No data available for backtesting.")
            return

        df = self.data.copy()
        df["macd"] = macd(df["close"],window_slow=30,window_fast=6,fillna=False)  #calcolo indicatore MACD fatto automaticamente da ta.trend.macd
        df["signal"] = np.where(df['macd'] > 0, 1, -1)

        if df['signal'].roll(window=2).diff() == 1:
            df['position'] = 1
        elif df['signal'].roll(window=2).diff() == 0:
            df['position'] = 0
        elif df['position'].roll(window=2).diff() == -1:
            df['position'] = -1



        return df
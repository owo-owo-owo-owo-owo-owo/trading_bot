import numpy as np
import pandas as pd
import config
import database
from database import Database


class Strategy:
    def __init__(self):
        self.db = Database()
        self.data = None

    def sma(self,short_window=config.SMA_SHORT_WINDOW,long_window=config.SMA_LONG_WINDOW):
        if self.data is None:
            print("No data available for backtesting.")
            return

        df = self.data.copy()
        df['SMA_short'] = df['close'].rolling(window=short_window).mean()  # calcolo del SMA
        df['SMA_long'] = df['close'].rolling(window=long_window).mean()

        # Generate signals
        df['signal'] = 0
        df['signal'][long_window:] = np.where(df['SMA_short'][long_window:] > df['SMA_long'][long_window:], 30, -30)
        df['position'] = df['signal'].rolling(window=2).sum()

        # Return the backtested DataFrame
        return df

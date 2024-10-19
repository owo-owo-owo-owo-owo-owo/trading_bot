from fileinput import close

import numpy as np
import pandas as pd
import config
import database
from config import STRATEGY
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
        df["position"] = macd(df["close"],window_slow=30,window_fast=6,fillna=False)

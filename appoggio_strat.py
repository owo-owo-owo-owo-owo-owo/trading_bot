from fileinput import close

import numpy as np
import pandas as pd
import config
import database
from config import STRATEGY
from database import Database
from ta.trend import macd
from ta.volatility import bollinger_hband_indicator

# Load data
db = Database()
data = None
df = data.copy()


# Add bollinger band high indicator filling nans values
df["bb_high_indicator"] = ta.volatility.bollinger_hband_indicator(
    df["Close"], window=20, window_dev=2, fillna=True
)

# Add bollinger band low indicator filling nans values
df["bb_low_indicator"] = ta.volatility.bollinger_lband_indicator(
    df["Close"], window=20, window_dev=2, fillna=True
)

print(df.columns)
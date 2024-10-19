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
        self.sma = self.I(talib.SMA, close, self.n)

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

'''
db = Database(db_name=config.DATABASE_NAME)
table_name = config.table_name
db.create_table(table_name)

results = db.fetch_data(table_name)
if results:
    print("data found in local database" '\n')
    ohlc_data = db.fetch_data(table_name)
if not results:
    # Fetch historical data
    fetcher = DataFetcher()
    ohlc_data = fetcher.fetch_ohlc(symbol=config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)

    # Insert data into the database
if ohlc_data:
    db.create_table(table_name)
    db.insert_data(table_name, ohlc_data)
    print(f"Inserted {len(ohlc_data)} rows into {table_name} table.", "\n")

table_name = config.table_name
raw_data = db.fetch_data(table_name)

# Create a pandas DataFrame
df = pd.DataFrame(raw_data, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
print(df)
df = df.drop(columns=['timestamp'])
print(df)
'''
db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
data = pd.read_csv(db)
data.columns = [column.capitalize() for column in data.columns]

bt = Backtest(data, simplestrat, cash=1000000, commission=.002)
stats = bt.run()
print(stats)
# main.py
from pandas.errors import SettingWithCopyWarning
from tensorflow.python.types.doc_typealias import document
from tensorflow.tools.docs.doc_controls import doc_in_current_and_subclasses

import config
from database import Database
from data_fetch import DataFetcher
from backtesting import Backtester
from ML_model import LSTMModel
import warnings

def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
    # Use configuration variables from config.py
    trading_symbol = config.TRADING_SYMBOL
    candlestick_duration = config.CANDLESTICK_DURATION
    data_limit = config.DATA_LIMIT
    
    # Initialize database
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
        ohlc_data = fetcher.fetch_ohlc(symbol=trading_symbol, interval=candlestick_duration, limit=data_limit)

    # Insert data into the database
    if ohlc_data:
        db.create_table(table_name)
        db.insert_data(table_name, ohlc_data)
        print(f"Inserted {len(ohlc_data)} rows into {table_name} table.", "\n")

    # Strategy selector

    if config.STRATEGY is not None:
            print(f"Running strategy {config.STRATEGY}" "\n")
            Backtester(symbol=trading_symbol, candlestick_duration=candlestick_duration).run_backtest()


    db.close()

if __name__ == '__main__':
    main()
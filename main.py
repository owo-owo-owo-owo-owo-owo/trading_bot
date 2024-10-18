# main.py
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
    # Use configuration variables from config.py
    trading_symbol = config.TRADING_SYMBOL
    time_frame = config.CANDLESTICK_DURATION
    data_limit = config.DATA_LIMIT
    
    # Initialize database
    db = Database(db_name=config.DATABASE_NAME)
    table_name = f'{trading_symbol}_{time_frame}'
    db.create_table(table_name)

    results = db.fetch_data(table_name)
    if results:
        print("data found in local database" '\n')
        ohlc_data = db.fetch_data(table_name)
    if not results:
    # Fetch historical data
        fetcher = DataFetcher()
        ohlc_data = fetcher.fetch_ohlc(symbol=trading_symbol, interval=time_frame, limit=data_limit)

    # Insert data into the database
    if ohlc_data:
        db.create_table(table_name)
        db.insert_data(table_name, ohlc_data)
        print(f"Inserted {len(ohlc_data)} rows into {table_name} table.", "\n")

    # Strategy selector
    if config.STRATEGY == 'SMA_Crossover':
        print("Running Simple Moving Average Crossover Backtest..." "\n")
        backtester = Backtester(symbol=trading_symbol, time_frame=time_frame)
        backtester.run_backtest()
    elif config.STRATEGY == 'LSTM_Prediction':
        print("Running LSTM Model Prediction..." "\n")
        # Initialize LSTM model and run prediction
        lstm_model = LSTMModel(time_frame=time_frame, model_name=config.MODEL_NAME)
        lstm_model.run()

    else:
        print(f"Strategy {config.STRATEGY} not recognized." "\n")

    db.close()

if __name__ == '__main__':
    main()

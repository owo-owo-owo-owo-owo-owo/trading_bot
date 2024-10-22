#calulate the vwap

import pandas as pd
import pandas_ta as ta
import config
from data_fetch import DataFetcher
''' 
functions stil to be added in this file for implementation to work:
- adjust_leverage_size_signal
- cancel_all_orders
- pnl_close
- ask_bid
- cancel_all_orders
- limit_order
'''

def calculate_vwap_with_wymbol(symbol):
    snapshot_data = DataFetcher(config.TRADING_SYMBOL, config.CANDLESTICK_DURATION, config.DATA_LIMIT)      #this should ber working  but must be tested in implementation_test to confirm. Errors should still be minimal and limited to class errors (market data not formatted as a dataframe)
    df = pd.read_csv(snapshot_data)

    #convert the timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    #ensure all columnes used for vwap calc are numeric
    numeric_columns = ['high', 'low', 'close', 'volume']
    for column in numeric_columns:
        df['column'] = pd.to_numeric(df['column'], errors='coerce')

    df.dropna(subset=numeric_columns, inplace=True)

    #ensure the df is ordered by datetime
    df.sort_index(inplace=True)
    df['vwap'] = ta.vwap(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])


    #latest vwap
    latest_vwap = df['vwap'].iloc[-1]

    return df, latest_vwap


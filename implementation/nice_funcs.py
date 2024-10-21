#calulate the vwap

import pandas as pd
import pandas_ta as ta


def calculate_vwap_with_wymbol(symbol):
    snapshot_data = get_ohlcv2(symbol, '10m', 300)
    df = process_data_to_df(snapshot_data)

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
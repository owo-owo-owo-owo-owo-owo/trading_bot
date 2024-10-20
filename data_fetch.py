# data_fetch.py
import pandas as pd
import requests
import config
import os

class DataFetcher:
    def fetch_ohlc(self, symbol=config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT):
        """
        Fetch OHLC data from the Binance API.
        :param symbol: Trading pair (default: 'BTCUSDT')
        :param interval: Time frame for candlesticks (default: '1m')
        :param limit: Number of data points to fetch (default: 500)
        :return: List of tuples with OHLCV data
        """
        url = f"{config.BINANCE_BASE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Extract relevant columns and format the data (timestamp, open, high, low, close, volume)
            ohlc_data = [(int(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4]), float(item[5])) for item in data]
            print("data retrieved successfully" "\n")

            data = pd.DataFrame(ohlc_data,columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

            data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

            # Define the CSV file name
            csv_filename = config.db_name

            # Check if the file already exists
            if not os.path.exists(csv_filename):
                # If the file doesn't exist, write the DataFrame to a new file with headers
                data.to_csv(csv_filename, index=True)
                print(f"File {csv_filename} created and data saved.")
            '''
            else:
                # If the file exists, append the data without writing the header again
                data.to_csv(csv_filename, mode='a', header=False, index=True)
                print(f"Data appended to {csv_filename}.")
            '''

            return csv_filename
        else:
            print(f"Error fetching data: {response.status_code}")
            return None


# data_fetch.py
import pandas as pd
import requests
import config
import os

class DataFetcher:
    def fetch_ohlc(self, symbol=config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT):

        csv_filename = config.db_name

        if os.path.exists(csv_filename):
            print('data already found in local archive', '\n')
            return csv_filename
        else:
            print('data not found in local archive, downloading it', '\n')
            url = f"{config.BINANCE_BASE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                # Extract relevant columns and format the data (timestamp, open, high, low, close, volume)
                ohlc_data = [
                    (int(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4]), float(item[5])) for
                    item in data]
                print("data retrieved successfully" "\n")

                data = pd.DataFrame(ohlc_data, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

                # Check if the file already exists
                if not os.path.exists(csv_filename):
                    # If the file doesn't exist, write the DataFrame to a new file with headers
                    data.to_csv(csv_filename, index=True)
                    print(f"File {csv_filename} created and data saved.")

                return csv_filename
            else:
                print(f"Error fetching data: {response.status_code}")
                return None
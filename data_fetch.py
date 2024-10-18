# data_fetch.py
import requests
import config

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
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # Extract relevant columns and format the data (timestamp, open, high, low, close, volume)
            ohlc_data = [(int(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4]), float(item[5])) for item in data]
            print("data retrieved successfully" "\n")
            return ohlc_data
        else:
            print(f"Error fetching data: {response.status_code}")
            return None


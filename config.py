# config.py


# Database Configuration
DATABASE_NAME = 'crypto_data.sqlite'

# Trading Configuration
TRADING_SYMBOL = 'ETHUSDT'  # The pair we are trading
TIME_FRAMES = ['1m', '5m', '15m', '1h']  # Supported time frames
CANDLESTICK_DURATION = '1d'  # time length of the candlesticks (kline api)
DATA_LIMIT = 1000  # Limit of historical data points to fetch
db_name = f'{TRADING_SYMBOL}_{CANDLESTICK_DURATION}_{DATA_LIMIT}.csv'

# Binance API Configuration
BINANCE_BASE_URL = 'https://api.binance.com/api/v3/klines'
API_KEY = ''  # Leave blank for now if using a public API (no key required)
API_SECRET = ''  # Leave blank for now

# Backtesting Configuration
INITIAL_CAPITAL = 1000000
COMMISSION = 0.002



# LSTM Model Configuration
LOOKBACK_PERIOD = 70  # Number of previous data points to look back
LSTM_EPOCHS = 5  # Number of training epochs
LSTM_BATCH_SIZE = 32  # Batch size for training the LSTM model
MODEL_NAME =f'MODEL_{TRADING_SYMBOL}_{CANDLESTICK_DURATION}_{LOOKBACK_PERIOD}_{LSTM_EPOCHS}_{LSTM_BATCH_SIZE}'  # Base name for saving the model
THRESHOLD = 0.6  # Threshold for the certainty required for trading decision

# Strategy Selection

STRATEGY = 'MACD_strat.macd'

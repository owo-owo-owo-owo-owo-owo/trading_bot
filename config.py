# config.py

# Database Configuration
DATABASE_NAME = 'crypto_data.sqlite'

# Trading Configuration
TRADING_SYMBOL = 'BTCUSDT'  # The pair we are trading
TIME_FRAMES = ['1m', '5m', '15m', '1h']  # Supported time frames
CANDLESTICK_DURATION = '1h'  # time lenght of the candlesticks (kline api)
DATA_LIMIT = 1000  # Limit of historical data points to fetch

# Binance API Configuration
BINANCE_BASE_URL = 'https://api.binance.com/api/v3/klines'
API_KEY = ''  # Leave blank for now if using a public API (no key required)
API_SECRET = ''  # Leave blank for now

# Backtesting Configuration
INITIAL_CAPITAL = 100  # Starting capital for backtesting
SMA_SHORT_WINDOW = 5  # Short window for SMA in the backtest strategy
SMA_LONG_WINDOW = 30  # Long window for SMA in the backtest strategy


# LSTM Model Configuration
LOOKBACK_PERIOD = 70  # Number of previous data points to look back
LSTM_EPOCHS = 5  # Number of training epochs
LSTM_BATCH_SIZE = 32  # Batch size for training the LSTM model
MODEL_NAME =f'MODEL_{TRADING_SYMBOL}_{CANDLESTICK_DURATION}_{LOOKBACK_PERIOD}_{LSTM_EPOCHS}_{LSTM_BATCH_SIZE}'  # Base name for saving the model
THRESHOLD = 0.6  # Threshold for the certainty required for trading decision

# Strategy Selection
STRATEGY = 'SMA_Crossover'  # Options: 'SMA_Crossover', 'LSTM_Prediction', 'Custom'

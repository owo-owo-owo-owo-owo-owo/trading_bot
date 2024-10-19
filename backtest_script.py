# backtest_script.py
from idlelib.iomenu import encoding

import numpy as np
import pandas as pd
from sqlalchemy import false

from sma_strat import SMA_strat
from macd_strat import MACD_strat



import config
from database import Database

class Backtester:
    def __init__(self, symbol=config.TRADING_SYMBOL):
        self.symbol = symbol
        self.db = Database()
        self.data = None

    def fetch_historical_data(self):
        """
        Fetch historical OHLC data from the database and convert it into a pandas DataFrame.
        """
        table_name = config.db_name
        raw_data = self.db.fetch_data(table_name)
        
        # Create a pandas DataFrame
        df = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp
        df.set_index('timestamp', inplace=True)
        self.data = df


    def calculate_performance(self, df):
        """
        Calculate performance metrics based on the trading signals.
        """
        initial_capital = config.INITIAL_CAPITAL  # Starting capital for backtesting
        df['pct change'] = df['close'].pct_change()
        df['strategy_returns'] = config.Bet * df['position'] * df['pct change']     #chi lo sa se sono davvero questi i ritorni (ne dubito)   #ho sistemato sopra forse ora da il risultato corretto

        # Calculate cumulative returns
        df['cumulative_returns'] = df['strategy_returns'].cumsum()
        final_return = (df['cumulative_returns'].iloc[-1] + 1) * initial_capital     #questa e sopra ok

        print(f"Final Portfolio Value: ${final_return:.2f}")
        print(f"Total Return: {((final_return - initial_capital) / initial_capital) * 100:.2f}%")


    def run_backtest(self):
        """
        Run the entire backtesting process.
        """
        self.fetch_historical_data()
        backtested_df = MACD_strat.macd(self)

        if backtested_df is not None:
         self.calculate_performance(backtested_df)
         backtested_df.to_csv('backtest_log.csv', sep='\t', index=False, encoding='utf-8')  #float_format='%.3f'
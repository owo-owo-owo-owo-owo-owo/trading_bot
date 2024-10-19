# main.py
from pandas.errors import SettingWithCopyWarning
#from tensorflow.python.types.doc_typealias import document
#from tensorflow.tools.docs.doc_controls import doc_in_current_and_subclasses
import pandas as pd
from backtesting import Backtest
import config
import example_strat
import new_backtester
from data_fetch import DataFetcher
import warnings
from new_backtester import run_backtest


def main():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

    trading_symbol = config.TRADING_SYMBOL
    candlestick_duration = config.CANDLESTICK_DURATION
    data_limit = config.DATA_LIMIT

    new_backtester.run_backtest()

if __name__ == '__main__':
    main()
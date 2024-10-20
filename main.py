from pandas.errors import SettingWithCopyWarning
import config
import new_backtester
import warnings
from new_backtester import run_backtest

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)

def main():

    trading_symbol = config.TRADING_SYMBOL
    candlestick_duration = config.CANDLESTICK_DURATION
    data_limit = config.DATA_LIMIT

    new_backtester.run_backtest()

if __name__ == '__main__':
    main()
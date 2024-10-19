import pandas as pd
from backtesting import Backtest
import config
import example_strat
from data_fetch import DataFetcher



def run_backtest():
    db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
    data = pd.read_csv(db)
    data.columns = [column.capitalize() for column in data.columns]

    bt = Backtest(data, example_strat.simplestrat, cash=config.INITIAL_CAPITAL, commission=config.COMMISSION)
    stats = bt.run()
    print(stats)
    bt.plot()

if __name__ == '__main__':
    run_backtest()
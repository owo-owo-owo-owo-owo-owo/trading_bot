import pandas as pd
from backtesting import Backtest
import config
import macd_strat
from data_fetch import DataFetcher
import example_strat
import sma_strat
import RSI_MA_crossover



def run_backtest():
    db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
    data = pd.read_csv(db)
    data.columns = [column.capitalize() for column in data.columns]
    data.index = pd.DatetimeIndex(data['Timestamp'])  # define index of the dataframe
    data = data.drop(columns=['Timestamp'])

    bt = Backtest(data, RSI_MA_crossover.RSI_MA_cross, cash=config.INITIAL_CAPITAL, commission=config.COMMISSION)
    #stats = bt.optimize(s=range(49, 60, 1),l=range(99, 101, 1),maximize='Equity Final [$]',constraint=lambda param: param.s < param.l)   #in range(a,b,c) a>c e nemmeno uguale
    print(bt.run())
    #print(stats._strategy,'\n')
    #print(stats['_trades'])

if __name__ == '__main__':
    run_backtest()
import pandas as pd
from backtesting import Backtest
import config
import macd_strat
from macd_strat import macd_cross
from data_fetch import DataFetcher
import example_strat
import sma_strat
import RSI_MA_crossover
import time

start_time = time.time()


def run_backtest():
    db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
    data = pd.read_csv(db)
    data.columns = [column.capitalize() for column in data.columns]
    data.index = pd.DatetimeIndex(data['Timestamp'])  # define index of the dataframe
    data = data.drop(columns=['Timestamp'])

    data.Open /= config.FRACTION_FACTOR
    data.High /= config.FRACTION_FACTOR
    data.Low /= config.FRACTION_FACTOR
    data.Close /= config.FRACTION_FACTOR
    data.Volume *= config.FRACTION_FACTOR

    bt = Backtest(data, macd_strat.macd_cross, cash=config.INITIAL_CAPITAL, commission=config.COMMISSION, margin=0.7)
    #stats = bt.optimize(RSI_overbought=range(1,100), RSI_oversold=range(1,100), time=range(3,20),maximize='Equity Final [$]',constraint=lambda param: param.RSI_oversold < param.RSI_overbought)   #in range(a,b,c) a>c e nemmeno uguale
    stats = bt.optimize(fast=range(6,18), slow=range(12,34), signal=range(3,9), offset=range(7,13), sl_k=range(101,108,1), tp_k=range(102,108,5), maximize='Equity Final [$]', constraint=lambda param: param.slow>param.fast)
    #backtest = bt.run()
    #bt.plot()
    #print(backtest)
    #print(backtest['_trades'].to_string())
    print(stats)
    print(stats._strategy,'\n')
    print(stats['_trades'])

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")


if __name__ == '__main__':
    run_backtest()
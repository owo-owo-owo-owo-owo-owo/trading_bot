import numpy as np
import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
import config
import talib
import pandas_ta as ta
from data_fetch import DataFetcher
import matplotlib.pyplot as plt


#db = DataFetcher.fetch_ohlc(config.TRADING_SYMBOL, interval=config.CANDLESTICK_DURATION, limit=config.DATA_LIMIT)
#data = pd.read_csv(db)

def md(close,  fast, slow, signal,offset):
    macd_data = ta.macd(close, fast, slow, signal, offset)
    return macd_data['MACD_12_26_7'], macd_data['MACDs_12_26_7'], macd_data['MACDh_12_26_7']


def long_ma(close, period):
    #close = data['Close']
    #period = 100
    long_ma = talib.SMA(close, period)
    return long_ma


class macd_cross(Strategy):

    period = 200

    fast = 12
    slow = 26
    signal = 7
    offset = 9


    def init(self):
        self.macd, self.macd_signal, self.macd_histogram = self.I(md,pd.Series(self.data.Close),self.fast, self.slow, self.signal, self.offset)
        self.ma = self.I(long_ma, pd.Series(self.data.Close), self.period)
        #print(f' macd normal, {self.macd}, macd histogram{self.macd_histogram} , macd signal {self.macd_signal}')

    def next(self):
            price = self.data.Close[-1]
            stop_loss = 1.02*(price - (price-self.ma[-1]))

            '''
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            USA IL FOTTUTISSIMO PUNTO PER I CAZZO DI NUMERI DECIMALI
            '''
            take_profit = price + 1.4 *(price-stop_loss)
            #print(stop_loss,'\n',price,'\n', take_profit, '\n')

            support = np.min(self.data.Close[-60:])
            resistance = np.max(self.data.Close[-60:])

            if (resistance-support/price) < 0.004:
                market_is_stagnant = False
            else:
                market_is_stagnant = True

            if not self.position:
                if market_is_stagnant == False:
                    if stop_loss < price < take_profit:
                        if self.macd[-1] > self.macd_signal[-1] and self.macd[-2] <= self.macd_signal[-2] and self.macd[-1] < 0:
                            self.buy(size=100,limit=price, sl=stop_loss, tp=take_profit)

                    elif stop_loss > price > take_profit:
                        if self.macd[-1] > 0 and self.macd[-1] < self.macd_signal and self.macd[-2] > self.macd_signal[-2]:
                            self.sell(size=100,limit=price, sl=stop_loss, tp=take_profit)

                elif market_is_stagnant == True:
                    if stop_loss < price < take_profit:
                        if self.macd[-1] > self.macd_signal[-1] and self.macd[-2] <= self.macd_signal[-2] and self.macd[
                            -1] < 0:
                            self.buy(size=100,limit=price, sl=stop_loss, tp=take_profit)

                    elif stop_loss > price > take_profit:
                        if self.macd[-1] > 0 and self.macd[-1] < self.macd_signal and self.macd[-2] > self.macd_signal[
                            -2]:
                            self.sell(size=100,limit=price, sl=stop_loss, tp=take_profit)

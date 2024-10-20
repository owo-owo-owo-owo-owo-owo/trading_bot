import numpy as np
import pandas as pd
from backtesting import Strategy
import config
import talib

'''
def I(self,
      func: (...) -> Any,
      *args: Any,
      name: Any = None,
      plot: bool = True,
      overlay: Any = None,
      color: Any = None,
      scatter: bool = False,
      **kwargs: Any) -> ndarray
'''
class MACD_strat(Strategy):
    n1 = 12
    n2 = 26
    n3 = 9

    def init(self):
        self.macd = self.I(talib.MACD, self.data.Close, self.n1, self.n2, self.n3)

    def next(self):
        if self.macd > 0:
            if self.position.is_long:
                self.position.close()
            else:
                self.sell()

        elif self.macd < 0:
            if self.position.is_short:
                self.position.close()
            else:
                self.buy()

import time

from pandas_ta import candle_color

import config
import utils
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.utils.types import (
    SIDES,  # <----
    Dict,
    L2BookMsg,  # <----
    L2BookSubscription,  # <----
    Literal,
    Optional,
    Side,  # <----
    TypedDict,
    Union,
    UserEventsMsg,  # <----
    UserEventsSubscription,  # <----
    Fill,
    CandleSubscription,
    OtherWsMsg


)


address, info, exchange = utils.setup()


class prova:
    def __init__(self):
        l2_book_subscription: L2BookSubscription = {"type": "l2Book", "coin": "SOL"}
        info.subscribe(l2_book_subscription, self.on_book_update)

        candle_subscription: CandleSubscription = {"type": "candle", "coin": "SOL","interval": "1m"}  # Replace "1m" with the desired interval
        info.subscribe(candle_subscription, self.on_candle_update)

    def on_book_update(self, book_msg: L2BookMsg) -> None:
        #book_data = book_msg["data"]['levels'][0]
        #book_data = book_msg["data"]
        levels = book_msg['data']['levels'][0]      #find the current price
        px = [level['px'] for level in levels]

        #print(px)

    def on_candle_update(self, candle_msg: OtherWsMsg) -> None:
        # Process candle updates (based on the channel specified)
        candle_data = candle_msg['data']
        candle_channel = candle_msg['channel']
        print(f"Candle update from {candle_channel}: {candle_data}")


def main():
    prova()


if __name__ == "__main__":
    main()
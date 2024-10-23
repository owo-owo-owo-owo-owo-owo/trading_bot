'''
example taken from the api of a basic adding strategy
only interested in the first part though
'''

import json
import logging
import threading
import time

import utils

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.utils.types import (
    SIDES,
    Dict,
    L2BookMsg,
    L2BookSubscription,
    Literal,
    Optional,
    Side,
    TypedDict,
    Union,
    UserEventsMsg,
    UserEventsSubscription,
)


# How far from the best bid and offer this strategy ideally places orders. Currently set to .3%
# i.e. if the best bid is $1000, this strategy will place a resting bid at $997
DEPTH = 0.003

# How far from the target price a resting order can deviate before the strategy will cancel and replace it.
# i.e. using the same example as above of a best bid of $1000 and targeted depth of .3%. The ideal distance is $3, so
# bids within $3 * 0.5 = $1.5 will not be cancelled. So any bids > $998.5 or < $995.5 will be cancelled and replaced.
ALLOWABLE_DEVIATION = 0.5

# The maximum absolute position value the strategy can accumulate in units of the coin.
# i.e. the strategy will place orders such that it can long up to 1 ETH or short up to 1 ETH
MAX_POSITION = 1.0

# The coin to add liquidity on
COIN = "ETH"

InFlightOrder = TypedDict("InFlightOrder", {"type": Literal["in_flight_order"], "time": int})
Resting = TypedDict("Resting", {"type": Literal["resting"], "px": float, "oid": int})
Cancelled = TypedDict("Cancelled", {"type": Literal["cancelled"]})
ProvideState = Union[InFlightOrder, Resting, Cancelled]


def side_to_int(side: Side) -> int:
    return 1 if side == "A" else -1


def side_to_uint(side: Side) -> int:
    return 1 if side == "A" else 0


class BasicAdder:
    def __init__(self, address: str, info: Info, exchange: Exchange):
        self.info = info
        self.exchange = exchange
        l2_book_subscription: L2BookSubscription = {"type": "l2Book", "coin": COIN}
        self.info.subscribe(l2_book_subscription, self.on_book_update)        #get info on the coin, args: 'what to get', how frequently to get it. in this example 'l2 book data' is asked, everytime there is a book update (l2book, trades, candle can be retrieved)
        user_events_subscription: UserEventsSubscription = {"type": "userEvents", "user": address}
        self.info.subscribe(user_events_subscription, self.on_user_events)
        self.position: Optional[float] = None
        self.provide_state: Dict[Side, ProvideState] = {
            "A": {"type": "cancelled"},
            "B": {"type": "cancelled"},
        }
        self.recently_cancelled_oid_to_time: Dict[int, int] = {}
        self.poller = threading.Thread(target=self.poll)
        self.poller.start()


#example continues but this is the interesting part

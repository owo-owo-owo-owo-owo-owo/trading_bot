import json

from termcolor import colored

import utils
from hyperliquid.utils import constants
import colorama


def get_position():
    address, info, exchange = utils.setup(base_url=constants.TESTNET_API_URL, skip_ws=True)

    # Get the user state and print out position information
    user_state = info.user_state(address)
    positions = []
    for position in user_state["assetPositions"]:
        positions.append(position["position"])
    if len(positions) > 0:
        print("positions:")
        for position in positions:
            print(json.dumps(position, indent=2))
    else:
        print(colored("no open positions", "black", "on_white"))


if __name__ == "__main__":
    get_position()
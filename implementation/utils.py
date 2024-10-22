import json
import os
import config
import eth_account
from eth_account.signers.local import LocalAccount

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info


def setup(base_url=None, skip_ws=False):

    account: LocalAccount = eth_account.Account.from_key(config.SECRET_KEY)

    address = account.address
    print("Running with account address:", address)     #derive the account address from the secret key if it is not inserted

    info = Info(base_url, skip_ws)
    user_state = info.user_state(address)
    spot_user_state = info.spot_user_state(address)
    margin_summary = user_state["marginSummary"]


    if float(margin_summary["accountValue"]) == 0 and len(spot_user_state["balances"]) == 0:     #no equity error (to be expected until funds are loaded to the account)
        print("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        error_string = f"No accountValue:\nIf you think this is a mistake, make sure that {address} has a balance on {url}.\nIf address shown is your API wallet address, update the config to specify the address of your account, not the address of the API wallet."
        raise Exception(error_string)

    #exchange = Exchange(account, base_url, account_address=address)
    '''
    dont know what the previous line does as commenting it does not affect behaviour in account_startup
    and it is the exact same as account_exchange = Exchange(account, constants.TESTNET_API_URL, account_address=address)
    in account_startup
    will investigate further and check if this creates any error in the long run
    '''

    return address, info
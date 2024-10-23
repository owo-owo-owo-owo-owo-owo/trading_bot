import eth_account
import utils
from eth_account.signers.local import LocalAccount
import config
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants


def account_startup():

    """
    Create an agent that can place trades on behalf of the account. The agent does not have permission to transfer
    or withdraw funds.
    """

    address, info, exchange = utils.setup(constants.TESTNET_API_URL, skip_ws=True)

    account: LocalAccount = eth_account.Account.from_key(config.SECRET_KEY)        #initialize a local account with the private key, stored in config.py
    print("Running with agent address:", account.address)
    exchange = Exchange(account, constants.TESTNET_API_URL, account_address=address)    # initialize exchange instance for the account

    user_state = info.user_state(address)  # returns info about user {'marginSummary': {'accountValue': '0.0', 'totalNtlPos': '0.0', 'totalRawUsd': '0.0', 'totalMarginUsed': '0.0'}, 'crossMarginSummary': {'accountValue': '0.0', 'totalNtlPos': '0.0', 'totalRawUsd': '0.0', 'totalMarginUsed': '0.0'}, 'crossMaintenanceMarginUsed': '0.0', 'withdrawable': '0.0', 'assetPositions': [], 'time': 1729687516203}

    return  account, exchange
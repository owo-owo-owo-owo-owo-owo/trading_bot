'''
implementazione presa pari pari da n vide yt
librerie da installare in aggiunta a quelle gia present:
- eth_account
- schedule
hyperliquid-python-sdk
'''
from ccxt import hyperliquid
#vwap market maker
from eth_account.signers.local import LocalAccount
import eth_account
import json
import time, random
from hyperliquid.info import Info  #exchange
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
import pandas as pd
import datetime
import schedule
import requests
import nice_funcs as n  #file che contiene le funzioni necessare per la strategia
#from dontshareconfig import secret   #Todo cambiare questo con i parametri su config


symbol = 'SOL'
timeframe = '5m'
sma_window = 2
lookback_days = 1

size = 1
max_loss = -6
target = 4
leverage = 4

def bot():
    account1 = LocalAccount = eth_account.Account.from_key(secret)
    positions1, im_in_pos, mypos_size, pos_syml, entry_px1, pnl_perc1, long1, num_of_pos = n.get_position(symbol,account1)
    print(f'these are position {symbol} {positions1} and we are in {num_of_pos} positions')

    lev, pos_size = n.adjust_leverage_size_signal(symbol, leverage, account1)

    if im_in_pos:
        n.cancel_all_orders(account1)
        print(f'we are in position {im_in_pos}')
        n.pnl_close(symbol, target, max_loss, account1)
    else:
        print('not in position so no pnl close')

    #get the price
    ask, bid, l2_data = n.ask_bid(symbol)

    bid11 = float(l2_data[0][10]['px'])
    ask11 = float(l2_data[1][10]['px'])

    #chekc if in partial positions
    if 0< mypos_size:
        print(f'current position size is {mypos_size} and we want to be at {pos_size}')
        pos_size = pos_size- mypos_size
        im_in_pos = False
    else:
        pos_size = pos_size

    #get vwap
    latest_vwap = n.calculate_vwap_with_symbol(symbol)[1]
    print([f'latest vwap is {latest_vwap}'])

    random_chance = random.random()

    if bid > latest_vwap:
        if random_chance <= .7:
            going_long = True
            print('going long')
        else:
            going_long = False
            print('not going long')

    else:
        if random_chance <= .3:
            going_long = True
            print('going long')
        else:
            going_long = False
            print([f'price is below vwap {bid} < {latest_vwap} and we are not going long'])


    if im_in_pos and going_long:
        n.cancel_all_orders(account1)
        print('canceled all orders')

        n.limit_order(symbol, True, pos_size, bid11, account1)
        print(f'placed limit order fro {symbol} at {bid11} size')

    elif not im_in_pos and not going_long:
        n.cancel_all_orders(account1)
        print('canceled all orders')

        n.limit_order(symbol, False, pos_size, ask11, account1)
        print(f'placed limit order for {symbol} at {ask11} fro {pos_size} size')

    else:
        print(f'no position for {symbol}')

schedule.every(3).seconds.do(bot())

from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime
import csv


print('Om Namahshivaya:')


# class TickData:

#     def __init__(self, watchlist)
#         self.candles = {}
#         self.ticks = {}
#         for instrument_token in watchlist:
#             candles[instrument_token] = pd.DataFrame()



# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')


previous_trading_day = (datetime.today() - BDay(1)).strftime('%Y-%m-%d')


def get_ltp(instrument_token):
    return kite.ltp(instrument_token)[str(instrument_token)]['last_price']

# def buy(instrument_token):
#     if instrument_token not in open_trades:
#         buy_price = get_ltp(instrument_token)
#         orderbook.write("Bought " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(buy_price))
#         open_trades.append(instrument_token)

# def sell(instrument_token):
#     if instrument_token in open_trades:
#         sell_price = get_ltp(instrument_token)
#         orderbook.write("Sold " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(sell_price) )
#         open_trades.remove(instrument_token)


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

nfo_instruments = pd.DataFrame(kite.instruments("NFO"))

banknifty_instruments = nfo_instruments.loc[(nfo_instruments.name == 'BANKNIFTY')]
# print(banknifty_instruments)
watchlist_dataframe = pd.DataFrame()
watchlist_dataframe.append(banknifty_instruments.loc[banknifty_instruments.strike == 35000, ['instrument_token', 'tradingsymbol']].head(2))
print(watchlist_dataframe)
watchlist_instruments = banknifty_instruments.loc[banknifty_instruments.strike == 35000, ['instrument_token', 'tradingsymbol']].head(2).values[0]
print(watchlist_instruments)

# call_instrument_token = nfo_instruments.loc[(nfo_instruments.n == )].instrument_token.values[0]
# put_instrument_token = nfo_instruments.loc[(nfo_instruments.tradingsymbol == put_tradingsymbol)].instrument_token.values[0]

import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime
import csv
print('Om Namahshivaya:')

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

def buy(instrument_token):
    if instrument_token not in open_trades:
        buy_price = get_ltp(instrument_token)
        orderbook.write("Bought " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(buy_price))
        open_trades.append(instrument_token)

def sell(instrument_token):
    if instrument_token in open_trades:
        sell_price = get_ltp(instrument_token)
        orderbook.write("Sold " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(sell_price) )
        open_trades.remove(instrument_token)


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


fno_stocks = open("/home/ubuntu/charlie/Support 200 DEMA/fno_stocks.txt")
fno_tradingsymbols = []
for symbol in fno_stocks.readlines():
    fno_tradingsymbols.append(symbol.strip())
print(fno_tradingsymbols)



instruments = pd.DataFrame(kite.instruments('NSE'))



# fno_instruments = nfo_instruments.loc[nfo_instruments.tradingsymbol.isin(fno_tradingsymbols)].instrument_token.tolist()
# watchlist = instruments.loc[instruments.tradingsymbol.isin(tradingsymbols)]
# print(fno_instruments)


ticker_dictionary = {260105:{'name':'BANKNIFTY', 'open_long_trade':False, 'open_short_trade':False, 'rsi_touchdown':False}}
fno_instruments = [260105]
for symbol in fno_tradingsymbols:
    kite_instrument_token = instruments.loc[instruments.tradingsymbol == symbol, 'instrument_token'].values[0]
    fno_instruments.append(kite_instrument_token)
    ticker_dictionary[kite_instrument_token] = {'name':symbol, 'open_long_trade':False, 'open_short_trade':False, '21_period_high':0, '21_period_low':0, 'rsi21_touchdown':False, 'rsi21_34_touchdown':False, 'rsi13_touchdown':False, 'rsi13_34_touchdown':False}

print(ticker_dictionary)
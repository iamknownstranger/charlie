print("Om Namahshivaya:")

import csv
from datetime import datetime
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint
from pandas.tseries.offsets import BDay
import talib
import pdb

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime("%Y:%m:%d %H:%M:%S")

previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

symbols = pd.read_csv("bse_nse_symbols.csv")
bse_symbols = symbols['bse_symbol']
nse_symbols = symbols['nse_symbol']

bse_instruments = pd.DataFrame(kite.instruments("BSE"))
nse_instruments = pd.DataFrame(kite.instruments("NSE"))


instrument_tokens = pd.DataFrame()

bse_listings = bse_instruments[bse_instruments.tradingsymbol.isin(bse_symbols)]
# print(bse_listings)
nse_listings = nse_instruments[nse_instruments.tradingsymbol.isin(nse_symbols)]
# print(nse_listings)
symbols['bse_token'] = ""
symbols['nse_token'] = ""
# symbols.loc[3, 'bse_token'] = 213
# print(symbols.loc[3, 'bse_token'])


for index, row in symbols.iterrows():
    
    # print(type(bse_instruments.loc[bse_instruments.tradingsymbol == row[0]].at['instrument_token']))
    # print(bse_instruments.loc[bse_instruments.tradingsymbol == row[0]].values[0][0])
    print(row[0], row[1] )
    try:
        symbols.loc[index, 'bse_token'] = bse_instruments.loc[bse_instruments.tradingsymbol == row[0]].values[0][0]
        symbols.loc[index, 'nse_token'] = nse_instruments.loc[nse_instruments.tradingsymbol == row[1]].values[0][0]
    except:
        continue
   
  
# print(symbols.isnull().sum(axis = 0))
print(symbols.to_csv("symbols.csv", index = False))



instrument_tokens['bse_token'] = bse_listings['instrument_token']
instrument_tokens['bse_tradingsymbol'] = bse_listings['tradingsymbol']

instrument_tokens['nse_token'] = nse_listings['instrument_token']
instrument_tokens['nse_tradingsymbol'] = nse_listings['tradingsymbol']

# instrument_tokens.to_csv("listed_on_both_exchanges.csv", index = False)

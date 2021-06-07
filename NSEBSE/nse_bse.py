print("Om Namahshivaya:")

import csv
from datetime import datetime
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint
from pandas.tseries.offsets import BDay
import talib

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


bse_instruments = pd.DataFrame(kite.instruments("BSE"))
nse_instruments = pd.DataFrame(kite.instruments("NSE"))

print(kite.instruments("BFO"))

# bse_instruments = bse_instruments[bse_instruments.lot_size == 1]
# bse_instruments = bse_instruments[bse_instruments.tick_size == 0.05]

# nse_instruments = nse_instruments[nse_instruments.lot_size == 1]
# nse_instruments = nse_instruments[nse_instruments.tick_size == 0.05]


combined = pd.merge(nse_instruments, bse_instruments, on='name')
combined.drop_duplicates(subset="instrument_token_x", keep=False, inplace=True)

combined.drop_duplicates(subset="instrument_token_y", keep=False, inplace=True)

combined.to_csv("nse_bse_instruments.csv", index =False)
print(combined[["instrument_token_x", "instrument_token_y","tradingsymbol_x", "tradingsymbol_y", "name"]].to_csv("nse_bse.csv", index = False))


nse_instruments = combined["instrument_token_x"]
print(len(nse_instruments))
print(len(bse_instruments))
bse_instruments = combined["instrument_token_y"]
print(nse_instruments)

for i in range(len(nse_instruments)):
    ltp_nse = kite.ltp(nse_instruments[i])[str(nse_instruments[i])]['last_price']
    ltp_bse = kite.ltp(bse_instruments[i])[str(bse_instruments[i])]['last_price']
    if(ltp_nse > ltp_bse):
        print("LTP is higher in NSE is greater than that in BSE")
        
    else:
        print("LTP is higher in BSE is greater than that in NSE")
    print("Differnece: ", ltp_nse - ltp_bse, ltp_nse, ltp_bse)

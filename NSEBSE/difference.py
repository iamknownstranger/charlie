print("Om Namahshivaya:")

import csv
from datetime import datetime
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint
from pandas.tseries.offsets import BDay
import talib
import numpy as np

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

stocks = pd.read_csv("symbols.csv")
stocks.dropna(inplace = True)

stocks['nse_token'] = stocks['nse_token'].astype(np.int32)
stocks['bse_token'] = stocks['bse_token'].astype(np.int32)

nse_instruments = stocks['nse_token']
print(type(nse_instruments))

bse_instruments = stocks['bse_token']
watchlist = []

# for i in stocks.index:
    
#     ltp_nse = kite.ltp(nse_instruments[i])[str(nse_instruments[i])]['last_price']
#     ltp_bse = kite.ltp(bse_instruments[i])[str(bse_instruments[i])]['last_price']

#     if(ltp_nse == ltp_nse):
#         print("=", end="")
#         continue
#     elif(ltp_nse > ltp_bse):
#         print("LTP is higher in NSE is greater than that in BSE")
        
        
#     else:
#         print("LTP is higher in BSE is greater than that in NSE")
#     print("Difference: ", ltp_nse - ltp_bse, ltp_nse, ltp_bse)

#     watchlist.append((nse_instruments[i], nse_instruments[i]))
# tradebook = open("tradebook.txt", "w")
# for nse_token, bse_token in watchlist:
#     ltp_nse = kite.ltp(nse_token)[str(nse_token)]['last_price']
#     ltp_bse = kite.ltp(bse_token)[str(bse_token)]['last_price']
#     tradebook.write("\n" + str(nse_token) + " nse ltp " +
#                         str(ltp_nse) + str(bse_token) + " bse ltp " + str(ltp_bse))



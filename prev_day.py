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

print(datetime.strftime("2021-05-31 15:16:00+05:30"))



# def get_timestamp():
#     return datetime.now(IST).strftime('%Y-%m-%d %X %z')

# print(get_timestamp())
# previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

# kite = Zerodha()

# # Set access token loads the stored session.
# # Name chosen to keep it compatible with kiteconnect.
# kite.set_access_token()

# token = 10393602

# data = pd.DataFrame(kite.historical_data(token, previous_trading_day +" 15:00:00", previous_trading_day + " 15:21:00","minute"))
# print(data)
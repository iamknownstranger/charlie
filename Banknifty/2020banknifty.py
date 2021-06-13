import csv
from datetime import datetime
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint
from pandas.tseries.offsets import BDay
import talib

# # get the standard UTC time
# UTC = pytz.utc

# # it will get the time zone
# # of the specified location
# IST = pytz.timezone('Asia/Kolkata')

# print(datetime.strftime("2021-05-31 15:16:00+05:30"))


# def get_timestamp():
#     return datetime.now(IST).strftime('%Y-%m-%d %X %z')

# print(get_timestamp())
# previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

token = 260105

year_data = pd.DataFrame(kite.historical_data(token, "2020-05-01 00:00:00", "2021-05-31 15:30:00","day"))
dates = year_data['date']
print(dates)

data = pd.DataFrame()
for date in dates:
    date = date.date()
    # print(date)
    data = data.append(pd.DataFrame(kite.historical_data(token, str(date) + " 09:21:00", str(date) + " 15:21:00","3minute")))

print(data)
print(data.to_csv("bn_01-05-20_31-05-20201.csv", index = False))
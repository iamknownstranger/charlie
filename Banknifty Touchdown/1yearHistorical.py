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

data = pd.DataFrame(kite.historical_data(token, "2020-05-01 00:00:00", "2021-05-31 15:30:00","day"))

prev_close = 0
prev_high = 0
prev_low = 0

higher_highs = 0
lower_lows = 0
touchdowns = 0
nahbroh = 0
pandl = 0

for row in data.iterrows():
    if row[1]['open'] >= prev_close:
        if row[1]['low'] < prev_close:
            print("touchdown")
        if row[1]['high'] >= prev_high:
            print("Higher High")
            if row[1]['close'] > prev_high:
                print("Closed above prev high")
            else:
                print("Closed below prev high")
                higher_highs += 1
    
        if row[1]['low'] <= prev_low:
            print("Lower low")
            if row[1]['close'] < prev_low:
                print("closed below prev_low")
                lower_lows + 1
        else:
            nahbroh += 1

    else:
        if row[1]['high'] > prev_close:
            print("touchdown")
        if row[1]['high'] >= prev_high:
            print("Higher High")
            if row[1]['close'] > prev_high:
                print("Closed above prev high")
            else:
                print("Closed below prev high")
                higher_highs += 1
    
        if row[1]['low'] <= prev_low:
            print("Lower low")
            if row[1]['close'] < prev_low:
                print("closed below prev_low")
                lower_lows + 1
        else:
            nahbroh += 1
    prev_close = row[1]['close']
    prev_high = row[1]['high']
    prev_low = row[1]['low']


from pandas.tseries.offsets import BDay
print("Om Namahshivaya:")

import csv
from datetime import datetime, timedelta
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


today = datetime.today()
previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

historical_data = kite.historical_data(
    260105, previous_trading_day, previous_trading_day, "day")
print(dict(historical_data[0])['high'])
print(historical_data)

# watchlist = [260105]
# # properties = {}



# today_data = ""
# historical_data = ""

# nse_instruments = pd.DataFrame(kite.instruments('NSE'))
# stock_instruments = nse_instruments.loc[nse_instruments.lot_size == 1]
# stock_instruments = nse_instruments.loc[nse_instruments.tick_size == 0.05] 

# watchlist = []
# stocks = {}

# for row in stock_instruments.iterrows():

#     instrument_token = row[1]['instrument_token']
#     stock_name = row[1]['tradingsymbol']

#     watchlist.append(instrument_token)
#     stocks[instrument_token] = stock_name
  
# print(stocks, watchlist)

# print("21 Day Range Breakout")
# for instrument_token in watchlist:


#     try:
#         historical_data = pd.DataFrame(kite.historical_data(
#             instrument_token, today - timedelta(days=34), today, "day"))
    
#         historical_data = historical_data.head(-1).tail(21)
       
#         todays_ohlc = kite.ohlc(instrument_token)[
#             str(instrument_token)]

#         last_price = todays_ohlc['last_price']
#         ohlc = todays_ohlc['ohlc']

#         today_high = ohlc['high']
#         today_low = ohlc['low']
        
        
#         historical_data['range'] = historical_data['high'] - historical_data['low']
#         max_range = historical_data['range'].max()
#         highest_high = historical_data['high'].max()
#         today_range = today_high - today_low

#         # Check if todays range is greater than the last 21 days
#         if today_range >= max_range:

#             # Check if closed above the high of the last 21 days
#             if last_price >= highest_high:
#                 print(instrument_token, stocks[str(instrument_token), today_range, max_range, last_price, highest_high])
#         else:
#             print('=', end="")
       
#     except:
#         continue

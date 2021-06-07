# from jugaad_trader import Zerodha


# import pytz
# from datetime import datetime

# import pandas as pd
# import csv


# kite = Zerodha()


# # Set access token loads the stored session.
# # Name chosen to keep it compatible with kiteconnect.
# kite.set_access_token()

# kws = kite.ticker()

# # get the standard UTC time
# UTC = pytz.utc

# # it will get the time zone
# # of the specified location
# IST = pytz.timezone('Asia/Kolkata')


# def get_timestamp():
#     return datetime.now(IST).strftime("%Y:%m:%d %H:%M:%S")



# watchlist = [10395650, 10395906]
# ltp144 = {}
# tick_data = {}

# for ticker in watchlist:
#   tick_data[ticker] = []
#   ltp144[ticker] = []


# instrument_token = ''
# ltp = ''

# csv_file1 = open(str(watchlist[0])+".csv", "w")
# csv_file2 = open(str(watchlist[1])+".csv", "w")
# writer1 = csv.writer(csv_file1)
# writer2 = csv.writer(csv_file2)

# csv_file3 = open(str(watchlist[0])+"_ltp.csv", "w")
# csv_file4 = open(str(watchlist[1])+"_ltp.csv", "w")
# writer3 = csv.writer(csv_file3)
# writer4 = csv.writer(csv_file4)

# tradebook = open('tradebook.txt', "w")
# orderbook = open("orderbook.txt", "w")


# def on_ticks(ws, ticks):
#     # Callback to receive ticks.
#     for tick in ticks:
#         instrument_token = tick['instrument_token']
#         ltp = tick['last_price']
#         ohlc = tick['ohlc']
#         if(ltp > ohlc['high']):
#             tradebook.write("\nBreakout " + str(instrument_token) + get_timestamp())
#         elif(ltp < ohlc['low']):
#             tradebook.write("\nBreakdown " + str(instrument_token) + get_timestamp())
#         if(instrument_token == watchlist[0]):
          
#             writer3.writerow([get_timestamp(), ltp, ohlc])
#         elif(instrument_token == watchlist[1]):
#             writer4.writerow([get_timestamp(), ltp, ohlc])
#         ltp144[instrument_token].append(ltp)
#         if(len(ltp144[instrument_token]) == 144):
#             if(instrument_token == watchlist[0]):
#                 print("LTP144")
#                 print([instrument_token, get_timestamp(), ltp144[instrument_token][0], max(ltp144[instrument_token]), min(ltp144[instrument_token]), ltp144[instrument_token][-1], ohlc])
#                 writer1.writerow([instrument_token, get_timestamp(), ltp144[instrument_token][0], max(ltp144[instrument_token]), min(ltp144[instrument_token]), ltp144[instrument_token][-1], ohlc])
          
#             elif(instrument_token == watchlist[1]):
#                 writer2.writerow([instrument_token, get_timestamp(), ltp144[instrument_token][0], max(ltp144[instrument_token]), min(ltp144[instrument_token]), ltp144[instrument_token][-1], ohlc])
#             else:
#                 continue
#             if(ltp144[instrument_token][-1] > ohlc['high']):
#                 orderbook.write("\nBreakout " + str(instrument_token) + get_timestamp())
#             elif(ltp144[instrument_token][-1] > ohlc['low']):
#                 orderbook.write("\nBreakdown " + str(instrument_token) + get_timestamp())
#             ltp144[instrument_token] = []


# def on_connect(ws, response):
#     # Callback on successful connect.
#     # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
#     ws.subscribe(watchlist)

#     # Set RELIANCE to tick in `full` mode.
#     ws.set_mode(ws.MODE_QUOTE, watchlist)


# def on_close(ws, code, reason):
#     # On connection close stop the event loop.
#     # Reconnection will not happen after executing `ws.stop()`
#     ws.stop()


# # Assign the callbacks.
# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close

# # Infinite loop on the main thread. Nothing after this will run.
# # You have to use the pre-defined callbacks to manage subscriptions.
# kws.connect()



from jugaad_trader import Zerodha


import pytz
from datetime import datetime

import pandas as pd
import csv


kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

kws = kite.ticker()

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime("%Y:%m:%d %H:%M:%S")



watchlist = [10395650, 10395906]
ltp144 = {}
tick_data = {}
trades = {}

for ticker in watchlist:
  tick_data[ticker] = []
  ltp144[ticker] = []
  trades[ticker] = {"breakout": False, "breakdown":True}


instrument_token = ''
ltp = ''

csv_file1 = open(str(watchlist[0])+".csv", "w")
csv_file2 = open(str(watchlist[1])+".csv", "w")
writer1 = csv.writer(csv_file1)
writer2 = csv.writer(csv_file2)

csv_file3 = open(str(watchlist[0])+"_ltp.csv", "w")
csv_file4 = open(str(watchlist[1])+"_ltp.csv", "w")
writer3 = csv.writer(csv_file3)
writer4 = csv.writer(csv_file4)

tradebook = open('tradebook.txt', "w")
orderbook = open("orderbook.txt", "w")


def on_ticks(ws, ticks):
    # Callback to receive ticks.
    for tick in ticks:
        instrument_token = tick['instrument_token']
        ltp = tick['last_price']
        ohlc = tick['ohlc']
        if(ltp > ohlc['high']):
            if(tradebook[instrument_token]["breakout"] == False):
                tradebook.write("\nBreakout " + str(instrument_token) + " " + get_timestamp())
                tradebook[instrument_token]["breakout"] = True
                tradebook[instrument_token]["breakdown"] = False

        elif(ltp < ohlc['low']):
            if(tradebook[instrument_token]["breakdown"] == False):

                tradebook.write("\nBreakdown " + str(instrument_token) + " " + get_timestamp())
                tradebook[instrument_token]["breakdown"] = False
                tradebook[instrument_token]["breakout"] = True
        if(instrument_token == watchlist[0]):
            writer3.writerow([get_timestamp(), ltp, ohlc])
        elif(instrument_token == watchlist[1]):
            writer4.writerow([get_timestamp(), ltp, ohlc])
        ltp144[instrument_token].append(ltp)
        if(len(ltp144[instrument_token]) == 144):
            if(instrument_token == watchlist[0]):
                writer1.writerow([instrument_token, get_timestamp(), ltp144[instrument_token][0], max(ltp144[instrument_token]), min(ltp144[instrument_token]), ltp144[instrument_token][-1], ohlc])
          
            elif(instrument_token == watchlist[1]):
                writer2.writerow([instrument_token, get_timestamp(), ltp144[instrument_token][0], max(ltp144[instrument_token]), min(ltp144[instrument_token]), ltp144[instrument_token][-1], ohlc])
            else:
                continue
            if(ltp144[instrument_token][-1] > ohlc['high']):
                orderbook.write("\nBreakout " + str(instrument_token) + get_timestamp())
            elif(ltp144[instrument_token][-1] > ohlc['low']):
                orderbook.write("\nBreakdown " + str(instrument_token) + get_timestamp())
            ltp144[instrument_token] = []


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(watchlist)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_QUOTE, watchlist)


def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()



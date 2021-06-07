import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime
import csv
print("Om Namahshivaya:")

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')


previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


banknifty_quote = kite.ltp(260105)['260105']
banknifty_spot = round(banknifty_quote['last_price'])

nfo_instruments = kite.instruments("NFO")

instruments = pd.DataFrame(nfo_instruments)


expiry = 'BANKNIFTY21610'
strike_lower_bound = banknifty_spot - (banknifty_spot % 100) - 500
strike_prices = [strike_price for strike_price in range(
    strike_lower_bound, strike_lower_bound+1000, 100)]

tradingsymbols = []
for strike in strike_prices:
    tradingsymbols.append(expiry+str(strike)+'CE')
    tradingsymbols.append(expiry+str(strike)+'PE')
print(tradingsymbols)

watchlist = instruments.loc[instruments.tradingsymbol.isin(
    tradingsymbols)].instrument_token.tolist()
watchlist.append(260105)


ticks144 = {}
volume144 = {}
tick_data = {}
candle_writers = {}
tick_writers = {}


for token in watchlist:
    ticks144[token] = []
    volume144[token] = 0
    tick_data[token] = pd.DataFrame(kite.historical_data(
        token, previous_trading_day + " 09:21:00", previous_trading_day + " 15:21:00", "3minute"))
    candle_writers[token] = csv.writer(open(str(token) + ".csv", "w"))
    tick_writers[token] = csv.writer(open(str(token) + "_ticks.csv", "w"))

tradebook = open('tradebook.txt', "w")
orderbook = open("orderbook.txt", "w")

instrument_token = ''
ltp = ''
rsi_touchdown = False
rsi_takeoff = False
open_positions = True


# kws = kite.ticker()


# def on_ticks(ws, ticks):

#     # Callback to receive ticks.
#     for tick in ticks:
#         instrument_token = tick['instrument_token']
#         ltp = tick['last_price']
#         ohlc = tick['ohlc']
#         last_quantity = tick['last_quantity']

#         if(ltp > ohlc['high']):
#             tradebook.write(
#                 "\nBreakout " + str(instrument_token) + get_timestamp())
#         elif(ltp < ohlc['low']):
#             tradebook.write("\nBreakdown " +
#                             str(instrument_token) + get_timestamp())

#         tick_writers[instrument_token].writerow(
#             [get_timestamp(), ltp, last_quantity, ohlc])

#         ticks144[instrument_token].append(ltp)
#         volume144[instrument_token] += last_quantity

#         if(len(ticks144[instrument_token]) == 144):
#             candle_open = ticks144[instrument_token][0]
#             candle_high = max(ticks144[instrument_token])
#             candle_low = min(ticks144[instrument_token])
#             candle_close = ticks144[instrument_token][-1]
#             candle_volume = volume144[instrument_token]
#             candle_data = [get_timestamp(), candle_open, candle_high,
#                            candle_low, candle_close, candle_volume, ohlc]

#             tick_data_length = len(tick_data[instrument_token])
#             tick_data[instrument_token].loc[tick_data_length] = candle_data
#             tick_data[instrument_token]['rsi21'] = talib.RSI(
#                 tick_data[instrument_token]['close'], timeperiod=21)
#             tick_data[instrument_token]['rsi13'] = talib.RSI(
#                 tick_data[instrument_token]['close'], timeperiod=13)
#             tick_data[instrument_token]['ema21'] = talib.EMA(
#                 tick_data[instrument_token]['close'], timeperiod=21)
#             tick_data[instrument_token]['wma21'] = talib.WMA(
#                 tick_data[instrument_token]['close'], timeperiod=21)

#             candle_writers[instrument_token].writerow(candle_data)

#             if(ticks144[instrument_token][-1] > ohlc['high']):
#                 tradebook.write(
#                     "\nBreakout " + str(instrument_token) + " closed above" + get_timestamp())
#             elif(ticks144[instrument_token][-1] > ohlc['low']):
#                 tradebook.write("\nBreakdown " +
#                                 str(instrument_token) + " closed below " + get_timestamp())

#             # RSI 21
#             candle = tick_data[instrument_token].iloc[-1]
#             rsi21 = candle['rsi21']
#             ema21 = candle['ema21']
#             rsi13 = candle['rsi13']

#             if(rsi21 < 21):
#                 tradebook.write("RSI 21 crossed below 21 " +
#                                 str(instrument_token))
#                 open_trades.append()

#             ticks144[instrument_token] = []
#             volume144[instrument_token] = 0


# def on_connect(ws, response):
#     # Callback on successful connect.
#     # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
#     ws.subscribe(watchlist)

#     # Set RELIANCE to tick in `full` mode.
#     ws.set_mode(ws.MODE_QUOTE, watchlist)


# def on_close(ws, code, reason):
#     # On connection close stop the event loop.
#     # Reconnection will not happen after executing `ws.stop()`
#     for token in watchlist:
#         tick_data[token].to_csv(str(token)+"_df.csv")
#     ws.stop()


# # Assign the callbacks.
# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close

# # Infinite loop on the main thread. Nothing after this will run.
# # You have to use the pre-defined callbacks to manage subscriptions.
# kws.connect()


for token in watchlist:
    tick_data[token]['rsi21'] = talib.RSI(tick_data[token].close, timeperiod = 14)
    print(tick_data[token].loc[tick_data[token].rsi21 <= 21])
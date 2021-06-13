print("Om Namahshivaya:")

import csv
from datetime import datetime
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint
from pandas.tseries.offsets import BDay
import talib
from _thread import start_new_thread

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

banknifty_quote = kite.quote(260105)['260105']
banknifty_spot = round(banknifty_quote['last_price'])
banknifty_close = round(banknifty_quote['ohlc']['close'])
banknifty_high = round(banknifty_quote['ohlc']['high'])
banknifty_low = round(banknifty_quote['ohlc']['low'])


if banknifty_spot > banknifty_close:
    call_strike = banknifty_close - (banknifty_close % 100)
    put_strike = banknifty_spot - (banknifty_spot % 100)
else:
    call_strike = banknifty_spot - (banknifty_spot % 100)
    put_strike = banknifty_close - (banknifty_close % 100)

expiry = "BANKNIFTY21617"
call_tradingsymbol = expiry + str(call_strike) + "CE"
put_tradingsymbol = expiry + str(put_strike) + "PE"
low_call_tradingsymbol = expiry + str(banknifty_low - (banknifty_low % 100)) + "CE"
high_put_tradingsymbol = expiry + str(banknifty_high - (banknifty_high % 100)) + "PE"

nfo_instruments = pd.DataFrame(kite.instruments("NFO"))

call_instrument_token = nfo_instruments.loc[(nfo_instruments.tradingsymbol == call_tradingsymbol)].instrument_token.values[0]
put_instrument_token = nfo_instruments.loc[(nfo_instruments.tradingsymbol == put_tradingsymbol)].instrument_token.values[0]
low_call_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == low_call_tradingsymbol)].instrument_token.values[0]
high_put_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == high_put_tradingsymbol)].instrument_token.values[0]

tradebook = open('tradebook.txt', 'w')
log = open('log.txt', 'w')
orderbook = open("orderbook.txt", 'w')

tickers = {call_instrument_token:call_tradingsymbol, put_instrument_token:put_tradingsymbol, low_call_instrument_token:low_call_tradingsymbol, high_put_instrument_token:high_put_tradingsymbol}
watchlist = []
for key in tickers.keys():
    watchlist.append(int(key))

ticks210 = {}
volume = {}
candles = {}
candle_writers = {}
tick_writers = {}

for instrument_token in watchlist:
    ticks210[instrument_token] = []
    volume[instrument_token] = 0
    candles[instrument_token] = pd.DataFrame(kite.historical_data(instrument_token, previous_trading_day +" 15:00:00", previous_trading_day + " 15:21:00", "minute"))
    candle_writers[instrument_token] = csv.writer(open(str(instrument_token) + ".csv", "w"))
    tick_writers[instrument_token] = csv.writer(open(str(instrument_token) + "_ticks.csv", "w"))


instrument_token = ''
ltp = ''

def on_candle(instrument_token, candles, ohlc):
    candles_df = candles[instrument_token].copy()

    candle_open = ticks210[instrument_token][0]
    candle_high = max(ticks210[instrument_token])
    candle_low = min(ticks210[instrument_token])
    candle_close = ticks210[instrument_token][-1]
    candle_volume = volume[instrument_token]
    candle_data = [get_timestamp(), candle_open, candle_high, candle_low, candle_close, candle_volume]
    
    candle_dataframe_length = len(candles[instrument_token])
    candles[instrument_token].loc[candle_dataframe_length] = candle_data
    candle_writers[instrument_token].writerow(candle_data)

    candles_df['rsi13'] = talib.RSI(candles_df['close'], timeperiod=13)
    candles_df['rsi21'] = talib.RSI(candles_df['close'], timeperiod=21)
    candles_df['rsi34'] = talib.RSI(candles_df['close'], timeperiod=34)
    candles_df['ema21'] = talib.EMA(candles_df['close'], timeperiod=21)
    candles_df['wma21'] = talib.WMA(candles_df['close'], timeperiod=21)

    if(candle_close > ohlc['high']):
        tradebook.write(
            "\nClose above Day High - Breakout " + str(instrument_token) + get_timestamp())
    elif(candle_close > ohlc['low']):
        tradebook.write("\nClose below days low - Breakdown " +
                        str(instrument_token) + get_timestamp())
    
    penultimate_candle = candles_df.iloc[-2]
    last_candle = candles_df.iloc[-1]
    symbol = tickers[instrument_token]

    if penultimate_candle.rsi34 > 66:
        if last_candle.close <= 66:
            tradebook.write(f"\n {symbol} Tookoff at 66 - 34 period RSI, ltp: { ltp}")
            print(symbol, "Touched at 34 period RSI")

    if penultimate_candle.rsi21 > 66:
        if last_candle.close <= 66:
            tradebook.write(f"\n {symbol} Tookoff at 79 - 21 period RSI, ltp: { ltp}")
            print(symbol, "Tookoff at 21 period RSI")

    if penultimate_candle.rsi13 > 79:
        if last_candle.close <= 79:
            tradebook.write(f"\n {symbol} Tookoff at 79 - 13 period RSI, ltp: { ltp}")
            print(symbol, "Tookoff at 21 period RSI")
    
    if penultimate_candle.rsi34 < 34:
        if last_candle.close >= 34:
            tradebook.write(f"\n {symbol} Tookoff at 34 - 34 period RSI, ltp: { ltp}")
            print(symbol, "Tookoff at 34 period RSI")

    if penultimate_candle.rsi21 < 34:
        if last_candle.close >= 34:
            tradebook.write(f"\n {symbol} Tookoff at 34 - 21 period RSI, ltp: { ltp}")
            print(symbol, "Tookoff at 34 period RSI")
    
    if penultimate_candle.rsi13 < 21:
        if last_candle.close >= 21:
            tradebook.write(f"\n {symbol} Tookoff at 21 - 13 period RSI, ltp: { ltp}")
            print(symbol, "Tookoff at 13 period RSI")

    ticks210[instrument_token] = []
    volume[instrument_token] = 0
    return

kws = kite.ticker()


def on_ticks(ws, ticks):

    # Callback to receive ticks.
    for tick in ticks: 
        instrument_token = tick['instrument_token']
        ltp = tick['last_price']
        ohlc = tick['ohlc']
        last_quantity = tick['last_quantity']
            

        if(ltp > ohlc['high']):
            tradebook.write(
                "\nORB Breakout " + str(instrument_token) + get_timestamp())
        elif(ltp < ohlc['low']):
            tradebook.write("\nORB Breakdown " +
                            str(instrument_token) + get_timestamp())

        
        tick_writers[instrument_token].writerow([get_timestamp(), ltp, last_quantity, ohlc])

        ticks210[instrument_token].append(ltp)
        volume[instrument_token] += last_quantity

        if(len(ticks210[instrument_token]) == 210):

            start_new_thread(on_candle, (instrument_token, candles, ohlc))


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here) .

    ws.subscribe(watchlist)

    # Set watchlist to tick in `Quote` mode.
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

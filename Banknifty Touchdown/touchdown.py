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

banknifty_quote = kite.quote(260105)['260105']
banknifty_spot = round(banknifty_quote['last_price'])
banknifty_close = round(banknifty_quote['ohlc']['close'])

if banknifty_spot > banknifty_close:
    call_strike = banknifty_close - (banknifty_close % 100)
    put_strike = banknifty_spot - (banknifty_spot % 100)
else:
    call_strike = banknifty_spot - (banknifty_spot % 100)
    put_strike = banknifty_close - (banknifty_close % 100)

expiry = "BANKNIFTY21603"
call_tradingsymbol = expiry + str(call_strike) + "CE"
put_tradingsymbol = expiry + str(put_strike) + "PE"


nfo_instruments = pd.DataFrame(kite.instruments("NFO"))
watchlist_instruments = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol.isin([call_tradingsymbol, put_tradingsymbol]))]
call_instrument_token, put_instrument_token = watchlist_instruments.instrument_token.tolist()

tradebook = open('tradebook.txt', "w")
orderbook = open("orderbook.txt", "w")

# tradebook.write(watchlist_instruments.name.tolist())


# Buy the call option
call_buy_price = kite.ltp(call_instrument_token)[
    str(call_instrument_token)]['last_price']

# Buy the put option
put_buy_price = kite.ltp(put_instrument_token)[
    str(put_instrument_token)]['last_price']

orderbook.write("Bought " + call_tradingsymbol + "at" + str(call_buy_price))
orderbook.write("Bought " + put_tradingsymbol + "at" + str(put_buy_price))

total_premium = call_buy_price + put_buy_price

tickers = {call_instrument_token:call_tradingsymbol, put_instrument_token:put_tradingsymbol}
watchlist = [call_instrument_token, put_instrument_token]

ticks144 = {}
volume144 = {}
tick_data = {}
candle_writers = {}
tick_writers = {}


for token in watchlist:
    ticks144[token] = []
    volume144[token] = 0
    tick_data[token] = pd.DataFrame(kite.historical_data(token, previous_trading_day +" 15:00:00", previous_trading_day + " 15:21:00", "minute"))
    candle_writers[token] = csv.writer(open(str(token) + ".csv", "w"))
    tick_writers[token] = csv.writer(open(str(token) + "_ticks.csv", "w"))

instrument_token = ''
ltp = ''
rsi_touchdown = False
rsi_takeoff = False
open_positions = True

kws = kite.ticker()


def on_ticks(ws, ticks):

    # Callback to receive ticks.
    for tick in ticks:
        instrument_token = tick['instrument_token']
        ltp = tick['last_price']
        ohlc = tick['ohlc']
        last_quantity = tick['last_quantity']
        
        if ltp > total_premium and open_positions:
            # Sell the call option
            call_sell_price = kite.ltp(call_instrument_token)[
                str(call_instrument_token)['last_price']]

            # Sell the put option
            put_sell_price = kite.ltp(put_instrument_token)[
                str(put_instrument_token)['last_price']]

            orderbook.write("Sold " + call_tradingsymbol +
                            "at" + str(call_sell_price))
            orderbook.write("Sold " + put_tradingsymbol +
                            "at" + str(put_sell_price))
            
            open_positions = False
            

        if(ltp > ohlc['high']):
            tradebook.write(
                "\nORB Breakout " + str(instrument_token) + get_timestamp())
        elif(ltp < ohlc['low']):
            tradebook.write("\nORB Breakdown " +
                            str(instrument_token) + get_timestamp())

        
        tick_writers[instrument_token].writerow([get_timestamp(), ltp, last_quantity, ohlc])

        ticks144[instrument_token].append(ltp)
        volume144[instrument_token] += last_quantity

        if(len(ticks144[instrument_token]) == 144):

            candle_open = ticks144[instrument_token][0]
            candle_high = max(ticks144[instrument_token])
            candle_low = min(ticks144[instrument_token])
            candle_close = ticks144[instrument_token][-1]
            candle_volume = volume144[instrument_token]
            candle_data = [get_timestamp(), candle_open, candle_high, candle_low, candle_close, candle_volume, ohlc]
            
            tick_data_length = len(tick_data[instrument_token])
            tick_data[instrument_token].loc[tick_data_length] = candle_data
            candle_writers[instrument_token].writerow(candle_data)

            tick_data['rsi13'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=13)
            tick_data['rsi21'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=21)
            tick_data['rsi34'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=34)
            tick_data['ema21'] = talib.ema_list(tick_data[instrument_token]['close'], timeperiod=21)
            tick_data['wma21'] = talib.wma_list(tick_data[instrument_token]['close'], timeperiod=21)

            if(ticks144[instrument_token][-1] > ohlc['high']):
                tradebook.write(
                    "\nClose above Day High - Breakout " + str(instrument_token) + get_timestamp())
            elif(ticks144[instrument_token][-1] > ohlc['low']):
                tradebook.write("\nClose below days low - Breakdown " +
                                str(instrument_token) + get_timestamp())
            
            penultimate_candle = tick_data.iloc[-2]
            last_candle = tick_data.iloc[-1]
            symbol = tickers[instrument_token]

            if penultimate_candle.rsi34 > 66:
                if last_candle.close <= 66:
                    tradebook.write("\n" + symbol + " Touched at 66 - 34 period RSI, ltp:", ltp)
                    print(symbol, "Touched at 34 period RSI")

            if penultimate_candle.rsi21 > 66:
                if last_candle.close <= 66:
                    tradebook.write("\n" + symbol + " Touched at 79 - 21 period RSI, ltp:", ltp)
                    print(symbol, "Tookoff at 21 period RSI")

            if penultimate_candle.rsi13 > 79:
                if last_candle.close <= 79:
                    tradebook.write("\n" + symbol + " Tookoff at 79 - 13 period RSI, ltp:", ltp)
                    print(symbol, "Tookoff at 21 period RSI")
            

            if penultimate_candle.rsi34 < 34:
                if last_candle.close >= 34:
                    tradebook.write("\n" + symbol + " Tookoff at 34 - 34 period RSI, ltp:", ltp)
                    print(symbol, "Tookoff at 34 period RSI")

            if penultimate_candle.rsi21 < 34:
                if last_candle.close >= 34:
                    tradebook.write("\n" + symbol + " Tookoff at 34 - 21 period RSI, ltp:", ltp)
                    print(symbol, "Tookoff at 34 period RSI")
            
            if penultimate_candle.rsi13 < 21:
                if last_candle.close >= 21:
                    tradebook.write("\n" + symbol + " Tookoff at 21 - 13 period RSI, ltp:", ltp)
                    print(symbol, "Tookoff at 13 period RSI")

            ticks144[instrument_token] = []
            volume144[instrument_token] = 0


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([call_instrument_token, put_instrument_token])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_QUOTE, [call_instrument_token, put_instrument_token])


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

import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime
import csv


print('Om Namahshivaya:')


# class TickData:

#     def __init__(self, watchlist)
#         self.candles = {}
#         self.ticks = {}
#         for instrument_token in watchlist:
#             candles[instrument_token] = pd.DataFrame()



# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')


previous_trading_day = (datetime.today() - BDay(1)).strftime('%Y-%m-%d')


def get_ltp(instrument_token):
    return kite.ltp(instrument_token)[str(instrument_token)]['last_price']

# def buy(instrument_token):
#     if instrument_token not in open_trades:
#         buy_price = get_ltp(instrument_token)
#         orderbook.write("Bought " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(buy_price))
#         open_trades.append(instrument_token)

# def sell(instrument_token):
#     if instrument_token in open_trades:
#         sell_price = get_ltp(instrument_token)
#         orderbook.write("Sold " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(sell_price) )
#         open_trades.remove(instrument_token)


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

banknifty_quote = kite.quote(260105)['260105']
banknifty_spot = round(banknifty_quote['last_price'])
banknifty_close = round(banknifty_quote['ohlc']['close'])
banknifty_high = round(banknifty_quote['ohlc']['high'])
banknifty_low = round(banknifty_quote['ohlc']['low'])

quotes = [banknifty_spot, banknifty_close, banknifty_high, banknifty_low]
nfo_instruments = pd.DataFrame(kite.instruments("NFO"))

banknifty_instruments = nfo_instruments.loc[(nfo_instruments.name == 'BANKNIFTY')]
# print(banknifty_instruments)
# watchlist_instruments = banknifty_instruments.loc[banknifty_instruments.strike == 35000]
# print(watchlist_instruments)

watchlist = []
tickertape = {}
strikes = []

for strike in range(banknifty_low, banknifty_high, 100):
    if strike not in strikes:
        strikes.append(strikes)
        monthly_options = banknifty_instruments.loc[banknifty_instruments.strike == strike, [
            'instrument_token', 'tradingsymbol']].head(2)
        call_instrument_token, call_tradingsymbol = monthly_options.values[0]
        put_instrument_token, put_tradingsymbol = monthly_options.values[1]
        tickertape[call_instrument_token] = call_tradingsymbol
        tickertape[put_instrument_token] = put_tradingsymbol
        watchlist.append(call_instrument_token)
        watchlist.append(call_instrument_token)

print(tickertape)

ticks210 = {}
volume = {}
candles = {}
candle_writers = {}
tick_writers = {}

for instrument_token in watchlist:
    ticks210[instrument_token] = []
    volume[instrument_token] = 0
    candles[instrument_token] = pd.DataFrame(kite.historical_data(instrument_token, previous_trading_day +" 15:00:00", previous_trading_day + " 15:21:00", "minute"))
    candle_writers[instrument_token] = csv.writer(open(tickertape[instrument_token] + ".csv", "w"))
    tick_writers[instrument_token] = csv.writer(open(tickertape[instrument_token] + "_ticks.csv", "w"))


tradebook = open('tradebook.txt', "w")
orderbook = open("orderbook.txt", "w")

instrument_token = ''
ltp = ''
open_positions = True

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

            last_candle = candles[instrument_token].iloc[-1]
            candle_open = ( last_candle.open + last_candle.close ) / 2
            candle_high = max(ticks210[instrument_token])
            candle_low = min(ticks210[instrument_token])
            candle_close = ticks210[instrument_token][-1]
            candle_close = (candle_open + candle_high + candle_low + candle_close) / 4
            candle_volume = volume[instrument_token]
            candle_data = [get_timestamp(), candle_open, candle_high, candle_low, candle_close, candle_volume]
            
            candle_dataframe_length = len(candles[instrument_token])
            candles[instrument_token].loc[candle_dataframe_length] = candle_data
            candle_writers[instrument_token].writerow(candle_data)

            candle_df = candles[instrument_token].copy()

            candle_df['rsi13'] = talib.RSI(candle_df['close'], timeperiod=13)
            candle_df['rsi21'] = talib.RSI(candle_df['close'], timeperiod=21)
            candle_df['rsi34'] = talib.RSI(candle_df['close'], timeperiod=34)
            candle_df['ema21'] = talib.EMA(candle_df['close'], timeperiod=21)
            candle_df['wma21'] = talib.WMA(candle_df['close'], timeperiod=21)

            if(ticks210[instrument_token][-1] > ohlc['high']):
                tradebook.write(
                    "\nClose above Day High - Breakout " + str(instrument_token) + get_timestamp())
            elif(ticks210[instrument_token][-1] > ohlc['low']):
                tradebook.write("\nClose below days low - Breakdown " +
                                str(instrument_token) + get_timestamp())
            
            penultimate_candle = candle_df.iloc[-2]
            last_candle = candle_df.iloc[-1]
            symbol = tickertape[instrument_token]

    
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

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(watchlist)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_QUOTE, watchlist)


def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    # for instrument_token in watchlist:
    #     candles[instrument_token].to_csv(tickertape[instrument_token]+"_df.csv")
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

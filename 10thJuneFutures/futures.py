import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime
import csv
print('Om Namahshivaya:')

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

tickers = {13613826: 'BANKNIFTY21JULFUT', 12417538: 'BANKNIFTY21JUNFUT'}


banknifty_quote = kite.quote(260105)['260105']
banknifty_future_ohlc = kite.ohlc(12417538)['12417538']
banknifty_spot = round(banknifty_quote['last_price'])
banknifty_close = round(banknifty_quote['ohlc']['close'])
banknifty_future_high = round(banknifty_future_ohlc['ohlc']['high'])
banknifty_future_low = round(banknifty_future_ohlc['ohlc']['low'])


if banknifty_spot > banknifty_close:
    call_strike = banknifty_close - (banknifty_close % 100)
    put_strike = banknifty_spot - (banknifty_spot % 100)
    
else:
    call_strike = banknifty_spot - (banknifty_spot % 100)
    put_strike = banknifty_close - (banknifty_close % 100)




expiry = "BANKNIFTY21610"
call_tradingsymbol = expiry + str(call_strike) + "CE"
put_tradingsymbol = expiry + str(put_strike) + "PE"
low_call_tradingsymbol = expiry + str(banknifty_future_low - (banknifty_future_low % 100)) + "CE"
high_put_tradingsymbol = expiry + str(banknifty_future_high - (banknifty_future_high % 100)) + "PE"

# option_tradingsymbols = [call_tradingsymbol, call_tradingsymbol, low_call_tradingsymbol, high_put_tradingsymbol]



nfo_instruments = pd.DataFrame(kite.instruments("NFO"))

# watchlist_instruments = nfo_instruments.loc[(nfo_instruments.name == 'BANKNIFTY') & (nfo_instruments.instrument_type == 'FUT'),]
# print(banknifty_future_instruments)

call_instrument_token = nfo_instruments.loc[(nfo_instruments.tradingsymbol == call_tradingsymbol)].instrument_token.values[0]
put_instrument_token = nfo_instruments.loc[(nfo_instruments.tradingsymbol == put_tradingsymbol)].instrument_token.values[0]

low_call_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == low_call_tradingsymbol)].instrument_token.values[0]
high_put_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == high_put_tradingsymbol)].instrument_token.values[0]

tickers[int(call_instrument_token)] = call_tradingsymbol
tickers[int(put_instrument_token)] = put_tradingsymbol
tickers[int(low_call_instrument_token)] = low_call_tradingsymbol
tickers[int(high_put_instrument_token)] = high_put_tradingsymbol


watchlist = list(tickers.keys())


ticks210 = {}
volume = {}
candles = {}
candle_writers = {}
tick_writers = {}

for instrument_token in watchlist:
    ticks210[instrument_token] = []
    volume[instrument_token] = 0
    candles[instrument_token] = pd.DataFrame(kite.historical_data(instrument_token, previous_trading_day +" 15:00:00", previous_trading_day + " 15:21:00", "minute"))
    candle_writers[instrument_token] = csv.writer(open(tickers[instrument_token] + ".csv", "w"))
    tick_writers[instrument_token] = csv.writer(open(tickers[instrument_token] + "_ticks.csv", "w"))


tradebook = open('tradebook.txt', "w")
orderbook = open("orderbook.txt", "w")

instrument_token = ''
ltp = ''
open_positions = True

# watchlist = [260105, 12783874, 13613826, 12417538, 12050178, 12056066, 12048130, 12062466]
# watchlist = [260105, 12783874, 13613826, 12417538, call_instrument_token, put_instrument_token, low_call_instrument_token, high_put_instrument_token]
# print(kite.ohlc(260105))

kws = kite.ticker()
print(watchlist)

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    for tick in ticks: 

        print(tick)
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

            candle_open = ticks210[instrument_token][0]
            candle_high = max(ticks210[instrument_token])
            candle_low = min(ticks210[instrument_token])
            candle_close = ticks210[instrument_token][-1]
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
    #     candles[instrument_token].to_csv(tickers[instrument_token]+"_df.csv")
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

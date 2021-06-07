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

def buy(instrument_token):
    if instrument_token not in open_trades:
        buy_price = get_ltp(instrument_token)
        orderbook.write("Bought " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(buy_price) )

def sell(instrument_token):
    if instrument_token in open_trades:
        sell_price = get_ltp(instrument_token)
        orderbook.write("Sold " + ticker_dictionary.get(instrument_token, 'No Key Found')['name'] + " at " + str(sell_price) )


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


banknifty_quote = get_ltp(260105)
banknifty_spot = round(banknifty_quote)

nfo_instruments = kite.instruments('NFO')

instruments = pd.DataFrame(nfo_instruments)


expiry = 'BANKNIFTY21610'
strike_lower_bound = banknifty_spot - (banknifty_spot % 100) - 500
strike_prices = [strike_price for strike_price in range(
    strike_lower_bound, strike_lower_bound+1000, 100)]

tradingsymbols = []
for strike in strike_prices:
    tradingsymbols.append(expiry+str(strike)+'CE')
    tradingsymbols.append(expiry+str(strike)+'PE')


ticker_dictionary = {260105:{'name':'BANKNIFTY', 'open_long_trade':False, 'open_short_trade':False, 'rsi_touchdown':False}}
watchlist = [260105]
for symbol in tradingsymbols:
    kite_instrument_token = instruments.loc[instruments.tradingsymbol == symbol, 'instrument_token'].values[0]
    watchlist.append(kite_instrument_token)
    ticker_dictionary[kite_instrument_token] = {'name':symbol, 'open_long_trade':False, 'open_short_trade':False, 'rsi21_touchdown':False, 'rsi21_34_touchdown':False, 'rsi13_touchdown':False, 'rsi13_34_touchdown':False}


ticks144 = {}
volume144 = {}
tick_data = {}
candle_writers = {}
tick_writers = {}




for token in watchlist:
    ticks144[token] = []
    volume144[token] = 0
    tick_data[token] = pd.DataFrame(kite.historical_data(
        token, previous_trading_day + ' 15:00:00', previous_trading_day + ' 15:21:00', 'minute'))
    print(type(tick_data[token].iloc[-2].low))
    print(tick_data[token].iloc[-2].low)
    candle_writers[token] = csv.writer(open(str(token) + '.csv', 'w'))
    tick_writers[token] = csv.writer(open(str(token) + '_ticks.csv', 'w'))


tradebook = open('tradebook.txt', 'w')
orderbook = open('orderbook.txt', 'w')


instrument_token = ''
ltp = ''
rsi_touchdown = False
rsi_takeoff = False

open_positions = False
open_trades = []


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
                '\nBreakout ' + str(instrument_token) + get_timestamp())
        elif(ltp < ohlc['low']):
            tradebook.write('\nBreakdown ' +
                            str(instrument_token) + get_timestamp())

        tick_writers[instrument_token].writerow(
            [get_timestamp(), ltp, last_quantity, ohlc])

        ticks144[instrument_token].append(ltp)
        volume144[instrument_token] += last_quantity

        ticker_data = ticker_dictionary[instrument_token]

        if(len(ticks144[instrument_token]) == 144):
            candle_open = ticks144[instrument_token][0]
            candle_high = max(ticks144[instrument_token])
            candle_low = min(ticks144[instrument_token])
            candle_close = ticks144[instrument_token][-1]
            candle_volume = volume144[instrument_token]
            candle_data = [get_timestamp(), candle_open, candle_high,
                           candle_low, candle_close, candle_volume, ohlc]

            tick_data_length = len(tick_data[instrument_token])
            tick_data[instrument_token].loc[tick_data_length] = candle_data
            tick_data[instrument_token]['rsi21'] = talib.RSI(
                tick_data[instrument_token]['close'], timeperiod=21)
            tick_data[instrument_token]['rsi13'] = talib.RSI(
                tick_data[instrument_token]['close'], timeperiod=13)
            tick_data[instrument_token]['ema21'] = talib.EMA(
                tick_data[instrument_token]['close'], timeperiod=21)
            tick_data[instrument_token]['wma21'] = talib.WMA(
                tick_data[instrument_token]['close'], timeperiod=21)

            candle_writers[instrument_token].writerow(candle_data)

            if(ticks144[instrument_token][-1] > ohlc['high']):
                tradebook.write(
                    '\nBreakout ' + str(instrument_token) + ' closed above' + get_timestamp())
            elif(ticks144[instrument_token][-1] > ohlc['low']):
                tradebook.write('\nBreakdown ' +
                                str(instrument_token) + ' closed below ' + get_timestamp())

            # RSI 21 

            candle = tick_data[instrument_token].iloc[-1]
            last_candle = tick_data[instrument_token].iloc[-2]

            rsi21 = candle['rsi21']
            ema21 = candle['ema21']
            rsi13 = candle['rsi13']

            if(rsi21 >= 21):
                if ticker_data['rsi21_touchdown']:
                    tradebook.write("RSI 21 bounced back" + ticker_data['name'] + ltp)
                    open_trades.append(instrument_token)
                    ticker_data['open_long_trade'] = True
                    open_positions = True
                    buy(instrument_token)
            
            elif(rsi21 <= 21):
                ticker_data['rsi21_touchdown'] = True
                tradebook.write("RSI 21 touched down 21" + ticker_data['name'] + ltp)

            if(rsi21 >= 34):
                if ticker_data['rsi21_34_touchdown']:
                    tradebook.write("RSI 21 bounced back from 34" + ticker_data['name'] + ltp)
                    open_trades.append(instrument_token)
                    ticker_data['open_long_trade'] = True
                    open_positions = True
                    buy(instrument_token)
            
            elif(rsi21 <= 34):
                ticker_data['rsi21_34_touchdown'] = True
                tradebook.write("RSI 21 touched down 34" + ticker_data['name'] + ltp)


            if(rsi13 >= 21):
                if ticker_data['rsi13_touchdown']:
                    tradebook.write("RSI 13 bounced back" + ticker_data['name'] + ltp)
                    open_trades.append(instrument_token)
                    ticker_data['open_long_trade'] = True
                    open_positions = True
                    buy(instrument_token)
            
            elif(rsi13 <= 21):
                ticker_data['rsi13_touchdown'] = True
                tradebook.write("RSI 13 touched down 21" + ticker_data['name'] + ltp)

            if(rsi13 >= 34):
                if ticker_data['rsi21_34_touchdown']:
                    tradebook.write("RSI 13 bounced back from 34" + ticker_data['name'] + ltp)
                    open_trades.append(instrument_token)
                    ticker_data['open_long_trade'] = True
                    open_positions = True
                    buy(instrument_token)
            
            elif(rsi13 <= 34):
                ticker_data['rsi13_34_touchdown'] = True
                tradebook.write("RSI 13 touched down 34" + ticker_data['name'] + ltp)

            if instrument_token in open_trades:
                if(candle_low < last_candle.low):
                    sell(instrument_token)

            ticks144[instrument_token] = []
            volume144[instrument_token] = 0


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(watchlist)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_QUOTE, watchlist)


def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    for token in watchlist:
        tick_data[token].to_csv(str(token)+'_df.csv')
    ws.stop()


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

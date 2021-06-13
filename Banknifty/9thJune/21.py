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
        orderbook.write("Bought " + ticker_dictionary.get(instrument_token,
                        'No Key Found')['name'] + " at " + str(buy_price))
        open_trades.append(instrument_token)


def sell(instrument_token):
    if instrument_token in open_trades:
        sell_price = get_ltp(instrument_token)
        orderbook.write("Sold " + ticker_dictionary.get(instrument_token,
                        'No Key Found')['name'] + " at " + str(sell_price))
        open_trades.remove(instrument_token)


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


ticker_dictionary = {260105: {'name': 'BANKNIFTY', 'open_long_trade': False,
                              'open_short_trade': False}}
tickers = {}
watchlist = [260105]
for symbol in tradingsymbols:
    kite_instrument_token = instruments.loc[instruments.tradingsymbol ==
                                            symbol, 'instrument_token'].values[0]
    watchlist.append(kite_instrument_token)
    tickers[kite_instrument_token] = symbol
    ticker_dictionary[kite_instrument_token] = {'name': symbol, 'open_long_trade': False, 'open_short_trade': False, '21_period_high': 0,
                                                '21_period_low': 0}


ticks210 = {}
volume210 = {}
tick_data = {}
candle_writers = {}
tick_writers = {}


for token in watchlist:
    ticks210[token] = []
    volume210[token] = 0
    tick_data[token] = pd.DataFrame(kite.historical_data(
        token, previous_trading_day + ' 15:00:00', previous_trading_day + ' 15:21:00', 'minute'))

    ticker_dictionary['21_period_high'] = tick_data[token].tail(21).max()
    ticker_dictionary['21_period_low'] = tick_data[token].tail(21).min()

    candle_writers[token] = csv.writer(open(str(token) + '.csv', 'w'))
    tick_writers[token] = csv.writer(open(str(token) + '_ticks.csv', 'w'))


tradebook = open('tradebook.txt', 'w')
orderbook = open('orderbook.txt', 'w')
log = open('log.txt', 'w')


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

        ticks210[instrument_token].append(ltp)
        volume210[instrument_token] += last_quantity

        ticker_data = ticker_dictionary[instrument_token]

        if(len(ticks210[instrument_token]) == 210):

            candle_open = ticks210[instrument_token][0]
            candle_high = max(ticks210[instrument_token])
            candle_low = min(ticks210[instrument_token])
            candle_close = ticks210[instrument_token][-1]
            candle_volume = volume210[instrument_token]
            candle_data = [get_timestamp(), candle_open, candle_high, candle_low, candle_close, candle_volume, ohlc]
            
            tick_data_length = len(tick_data[instrument_token])
            tick_data[instrument_token].loc[tick_data_length] = candle_data
            candle_writers[instrument_token].writerow(candle_data)

            tick_data['rsi13'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=13)
            tick_data['rsi21'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=21)
            tick_data['rsi34'] = talib.rsi_list(tick_data[instrument_token]['close'], timeperiod=34)
            tick_data['ema21'] = talib.ema_list(tick_data[instrument_token]['close'], timeperiod=21)
            tick_data['wma21'] = talib.wma_list(tick_data[instrument_token]['close'], timeperiod=21)

            if(ticks210[instrument_token][-1] > ohlc['high']):
                tradebook.write(
                    "\nClose above Day High - Breakout " + str(instrument_token) + get_timestamp())
            elif(ticks210[instrument_token][-1] > ohlc['low']):
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

            ticks210[instrument_token] = []
            volume210[instrument_token] = 0


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

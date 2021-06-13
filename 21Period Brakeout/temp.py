# from _thread import start_new_thread

# tickers = {2:[1,2,3,4], 4:[1,2,3,4]}


# def get_sum(key):
#     tickers[3] = [4,3,2,1]
#     print(sum(tickers[key]))

# for key in tickers.keys():

#     start_new_thread(get_sum, (key, )) 

# print(tickers)


from jugaad_trader import Zerodha
import pandas as pd
import datetime

kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


tickers = {260105: 'BANKNIFTY', 12783874: 'BANKNIFTY21AUGFUT',
           13613826: 'BANKNIFTY21JULFUT', 12417538: 'BANKNIFTY21JUNFUT'}

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


expiry = "BANKNIFTY21610"
call_tradingsymbol = expiry + str(call_strike) + "CE"
put_tradingsymbol = expiry + str(put_strike) + "PE"
low_call_tradingsymbol = expiry + \
    str(banknifty_low - (banknifty_low % 100)) + "CE"
high_put_tradingsymbol = expiry + \
    str(banknifty_high - (banknifty_high % 100)) + "PE"


nfo_instruments = pd.DataFrame(kite.instruments("NFO"))

# banknifty_future_instruments = nfo_instruments.loc[(nfo_instruments.name == 'BANKNIFTY') & (nfo_instruments.instrument_type == 'FUT'),]

call_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == call_tradingsymbol)].instrument_token.values[0]
put_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == put_tradingsymbol)].instrument_token.values[0]

low_call_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == low_call_tradingsymbol)].instrument_token.values[0]
high_put_instrument_token = nfo_instruments.loc[(
    nfo_instruments.tradingsymbol == high_put_tradingsymbol)].instrument_token.values[0]

tickers[call_instrument_token] = call_tradingsymbol
tickers[put_instrument_token] = put_tradingsymbol
tickers[low_call_instrument_token] = low_call_tradingsymbol
tickers[high_put_instrument_token] = high_put_tradingsymbol

watchlist = list(tickers.keys())
print(watchlist)


print(datetime.datetime.now())

kws = kite.ticker()


def on_ticks(ws, ticks):
    # Callback to receive ticks.
    for tick in ticks:
        print(tick )
        print("\n\n\n")


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([260105, 12783874, 13613826, 12417538, 12050178, 12056066, 12048130, 12062466])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [260105, 12783874, 13613826,
                12417538, 12050178, 12056066, 12048130, 12062466])


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



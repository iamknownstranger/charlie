import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime, timedelta, date
import csv
from ta.volume import volume_weighted_average_price


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


def get_historical_data(instrument, inception_date, interval):
    """extracts historical data and outputs in the form of dataframe
       inception date string format - dd-mm-yyyy"""
    from_date = datetime.strptime(inception_date, '%d-%m-%Y')
    to_date = date.today()
    data = pd.DataFrame(
        columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    while True:
        if from_date.date() >= (date.today() - timedelta(100)):
            data = data.append(pd.DataFrame(kite.historical_data(
                instrument, from_date, date.today(), interval)), ignore_index=True)
            break
        else:
            to_date = from_date + timedelta(100)
            data = data.append(pd.DataFrame(kite.historical_data(
                instrument, from_date, to_date, interval)), ignore_index=True)
            from_date = to_date
    data.set_index("date", inplace=True)
    return data


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


fno_stocks = open("/home/ubuntu/charlie/Support 200 DEMA/fno_stocks.txt")
fno_tradingsymbols = []
for symbol in fno_stocks.readlines():
    fno_tradingsymbols.append(symbol.strip())
# print(fno_tradingsymbols)

instruments = pd.DataFrame(kite.instruments('NSE'))
index = {}
for symbol in fno_tradingsymbols:
    kite_instrument_token = instruments.loc[instruments.tradingsymbol ==
                                            symbol, 'instrument_token'].values[0]
    index[kite_instrument_token] = symbol
print(index)
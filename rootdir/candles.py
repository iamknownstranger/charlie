from jugaad_trader import Zerodha
# from mpl_finance import candlestick_ohlc
# import matplotlib.pyplot as plt
import pytz
import datetime as dt
from pprint import pprint
from datetime import datetime
import pandas as pd
import numpy as np

# from candle import Candle 
import csv

kite = Zerodha()

# bank_nifty_spot = kite.ltp(260105)['260105']['last_price']
# print(bank_nifty_spot)



# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


# def get_from_():
    # return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")
    

today = dt.date.today()
# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


# candles = pd.DataFrame(kite.historical_data(15802114, today, get_timestamp(),"3minute"))

candles = pd.DataFrame(kite.historical_data(10395650, "2021-05-28 09:21:00", "2021-05-28 15:21:00","3minute"))

# print(candles.head())

def heikinashi(candles):
    candles_ha = candles.copy()
    for i in range(candles_ha.shape[0]):
        if i > 0:
            candles_ha.loc[candles_ha.index[i],'open'] = (candles['open'][i-1] + candles['close'][i-1])/2
      
        candles_ha.loc[candles_ha.index[i],'close'] = (candles['open'][i] + candles['close'][i] + candles['low'][i] +  candles['high'][i])/4
    candles_ha = candles_ha.iloc[1:,:]
    return candles_ha

heikin_df = heikinashi(candles)
# print(heikin_df.head())

# def RSI(series, period):
#     delta = series.diff().dropna()
#     u = delta * 0
#     d = u.copy()
#     u[delta > 0] = delta[delta > 0]
#     d[delta < 0] = -delta[delta < 0]
#     u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
#     u = u.drop(u.index[:(period-1)])
#     d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
#     d = d.drop(d.index[:(period-1)])
#     rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
#          pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
#     return 100 - 100 / (1 + rs)

# print("RSI 21", RSI(heikin_df.close, 21))

def rsi(serie, n):

    diff_serie = serie.diff()
    cumsum_incr = diff_serie.where(lambda x: x.gt(0), 0).cumsum()
    cumsum_decr = diff_serie.where(lambda x: x.lt(0), 0).abs().cumsum()
    rs_serie = cumsum_incr.div(cumsum_decr)
    rsi = rs_serie.mul(100).div(rs_serie.add(1)).fillna(0)

    return rsi

print("RSI 21", rsi(heikin_df.close, 21))



# def plot_chart(df):
#   fig, ax = plt.subplots()
#   candlestick_ohlc(ax,df.values,width=0.6, \
#                    colorup='green', colordown='red', alpha=0.8)
#   fig.tight_layout()
#   fig.show()

# plot_chart(heikin_df)





import plotly.graph_objects as go
import matplotlib.pyplot as plt
import mplfinance as mpf

import pandas as pd
import talib


df = pd.read_csv("210_10393090_ticks.csv", parse_dates=True)

# df.DateTime = pd.to_datetime(df.DateTime, errors = 'coerce')

df.set_index(pd.DatetimeIndex(df.DateTime), inplace=True)
print(df.DateTime)
 
# df['rsi'] = talib.RSI(df['close'], timeperiod=21)
# df['ema'] = talib.EMA(df['close'], timeperiod=21)

mpf.plot(df)


# df = heikinashi(candles_df)

# fig = go.Figure(data=go.Ohlc(x=df['datetime'],
#                 open=df['open'],
#                 high=df['high'],
#                 low=df['low'],
#                 close=df['close']))
# print(fig)
# df['rsi'].plot(ax=fig)

# fig.update(layout_xaxis_rangeslider_visible=False)
# fig.write_image("chart3.png")

# fig.show()


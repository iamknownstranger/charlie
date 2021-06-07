import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import mplfinance as fplt
import mplfinance as mpf

data = pd.read_csv("/home/ubuntu/charlie/bn_01-05-20_31-05-20201.csv")
data.index = data["date"].apply(lambda x: pd.Timestamp(x))
data.drop("date", axis=1, inplace=True)


mpf.plot(data,type="line", savefig='banknifty.png')



# def get_indicators(data):
#     # Get MACD
#     data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(
#         data['close'])

#     # Get MA10 and MA30
#     data["ema21"] = talib.EMA(data["close"], timeperiod=21)
#     data["ma21"] = talib.MA(data["close"], timeperiod=21)

#     # Get RSI
#     data["rsi"] = talib.RSI(data["close"])
#     return data

# with_indicators_data = get_indicators(data)


# def plot_chart(data, n, ticker):
    
#     # Filter number of observations to plot
#     data = data.iloc[-n:]
    
#     # Create figure and set axes for subplots
#     fig = plt.figure()
#     fig.set_size_inches((20, 16))
#     ax_candle = fig.add_axes((0, 0.72, 1, 0.32))
#     ax_macd = fig.add_axes((0, 0.48, 1, 0.2), sharex=ax_candle)
#     ax_rsi = fig.add_axes((0, 0.24, 1, 0.2), sharex=ax_candle)
#     ax_vol = fig.add_axes((0, 0, 1, 0.2), sharex=ax_candle)
    
#     # Format x-axis ticks as dates
#     ax_candle.xaxis_date()
    
#     # Get nested list of date, open, high, low and close prices
#     ohlc = []
#     for date, row in data.iterrows():
#         openp, highp, lowp, closep = row[:4]
#         ohlc.append([date2num(date), openp, highp, lowp, closep])
 
#     # Plot candlestick chart
#     ax_candle.plot(data.index, data["ema21"], label="EMA21")
#     ax_candle.plot(data.index, data["ma21"], label="MA21")
#     candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r", width=0.8)
#     ax_candle.legend()
    
#     # Plot MACD
#     ax_macd.plot(data.index, data["macd"], label="macd")
#     ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
#     ax_macd.plot(data.index, data["macd_signal"], label="signal")
#     ax_macd.legend()
    
#     # Plot RSI
#     # Above 70% = overbought, below 30% = oversold
#     ax_rsi.set_ylabel("(%)")
#     ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
#     ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
#     ax_rsi.plot(data.index, data["rsi"], label="rsi")
#     ax_rsi.legend()
    
#     # Show volume in millions
#     ax_vol.bar(data.index, data["volume"] / 1000000)
#     ax_vol.set_ylabel("(Million)")
   
#     # Save the chart as PNG
#     fig.savefig("charts/" + ticker + ".png", bbox_inches="tight")
    
#     plt.show()

# plot_chart(with_indicators_data, 269, "BankNifty")

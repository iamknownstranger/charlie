import pandas as pd
import talib as ta

df = pd.read_csv("charlie/rootdir/pe_ticks.csv")

df['rsi'] = ta.RSI(df['close'], timeperiod=21)
df['ema'] = ta.EMA(df['close'], timeperiod=21)
df['wma'] = ta.WMA(df['close'], timeperiod=21)
print(df.tail(21))

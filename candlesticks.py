import pandas as pd
import csv

ticks = pd.read_csv("10393090_ticks.csv")
ticks.columns = ["timestamp", "last_price", "last_quantity", "ohlc"]
ticks_list = ticks['last_price']

import pandas as pd

def batch(iterable, batch_number=10):
    """
    split an iterable into mini batch with batch length of batch_number
    supports batch of a pandas dataframe
    usage:
        for i in batch([1,2,3,4,5], batch_number=2):
            print(i)
        
        for idx, mini_data in enumerate(batch(df, batch_number=10)):
            print(idx)
            print(mini_data)
    """
    l = len(iterable)

    for idx in range(0, l, batch_number):
        if isinstance(iterable, pd.DataFrame):
            # dataframe can't split index label, should iter according index
            yield iterable.iloc[idx:min(idx+batch_number, l)]
        else:
            yield iterable[idx:min(idx+batch_number, l)]

csv_writer = csv.writer(open("210_10393090_ticks.csv", "w"))

candles = pd.DataFrame()
for chunk in batch(ticks, 210):
    timestamp = chunk.timestamp.iloc[-1]
    candle_open = chunk.last_price.iloc[0]
    candle_high = chunk.last_price.max()
    candle_low = chunk.last_price.min()
    candle_close = chunk.last_price.iloc[-1]
    volume = chunk.last_quantity.sum()
    csv_writer.writerow([timestamp, candle_open, candle_high, candle_low, candle_close, volume])
    print({"timestamp":timestamp, "open":candle_open, "high":candle_high, "low":candle_low, "close":candle_close, "volume":volume})
    candles.append({"timestamp":timestamp, "open":candle_open, "high":candle_high, "low":candle_low, "close":candle_close, "volume":volume}, ignore_index = True)

print(candles.head())
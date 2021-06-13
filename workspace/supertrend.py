from pandas.tseries.offsets import BDay
print("Om Namahshivaya:")

import csv
from datetime import datetime, timedelta
import pytz
import pandas as pd
from jugaad_trader import Zerodha
from pprint import pprint



today = datetime.today() 
previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

def eATR(Data, atr_lookback, high, low, close, whereTR):
 
    # TR
    for i in range(len(Data)):
        try:
    
            Data[i, whereTR] = max(Data[i, high] - Data[i, low],
            abs(Data[i, high] - Data[i - 1, close]),
            abs(Data[i, low] - Data[i - 1, close]))
        
        except ValueError:
            pass
    Data[0, whereTR] = 0 
    Data = ema(Data, 2, atr_lookback, whereTR, whereTR + 1, whereTR + 2)
    return Data


def supertrend(Data, multiplier, lookback):
    
    for i in range(len(Data)):
        
            # Average Price
            print(Data[i, 1])
            Data[i, 5] = (Data[i, 1] + Data[i, 2]) / 2
            # Basic Upper Band
            Data[i, 6] = Data[i, 5] + (multiplier * Data[i, 4])
            # Lower Upper Band
            Data[i, 7] = Data[i, 5] - (multiplier * Data[i, 4])
    
    # Final Upper Band
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, 8] = 0
            
        else:  
            if (Data[i, 6] < Data[i - 1, 8]) or (Data[i - 1, 3] > Data[i - 1, 8]):
                Data[i, 8] = Data[i, 6]
            
            else:
                Data[i, 8] = Data[i - 1, 8]
    
    # Final Lower Band
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, 9] = 0
            
        else:  
            if (Data[i, 7] > Data[i - 1, 9]) or (Data[i - 1, 3] < Data[i - 1, 9]):
                Data[i, 9] = Data[i, 7]
            
            else:
                Data[i, 9] = Data[i - 1, 9]
      
    # SuperTrend
    for i in range(len(Data)):
        
        if i == 0:
            Data[i, 10] = 0
        
        elif (Data[i - 1, 10] == Data[i - 1, 8]) and (Data[i, 3] <= Data[i, 8]):
            Data[i, 10] = Data[i, 8]
        
        elif (Data[i - 1, 10] == Data[i - 1, 8]) and (Data[i, 3] > Data[i, 8]):
            Data[i, 10] = Data[i, 9]
        
        elif (Data[i - 1, 10] == Data[i - 1, 9]) and (Data[i, 3] >= Data[i, 9]):
            Data[i, 10] = Data[i, 9]
        
        elif (Data[i - 1, 10] == Data[i - 1, 9]) and (Data[i, 3] < Data[i, 9]):
            Data[i, 10] = Data[i, 8]        
    
    return Data


historical_data = pd.DataFrame(kite.historical_data(260105, today - timedelta(days=34), today, "day"))
print(supertrend(historical_data, 21, 3))

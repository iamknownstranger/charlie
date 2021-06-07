import pandas as pd

ce = pd.read_csv("charlie/10393090_ticks.csv")
pe = pd.read_csv("charlie/10394882_ticks.csv")

# print(ce.last_price, pe.last_price)

total_premium = 474 
# percentile21 = total_premium * 0.21
# percentile13 = total_premium * 0.13
# target = total_premium + percentile21
# stoploss = total_premium - percentile13
# trailing_stoploss = total_premium + percentile13

target = total_premium + 21
stoploss = total_premium - 13

for tick in range(len(ce.last_price)):
    premium = ce.last_price[tick] 
    # print(premium)
    if(premium >= target):
        print("Target achieved", target)
        stoploss += 21
        target += 21
 
    elif(premium <= stoploss):
        print("Stoploss Hit", stoploss)
        break


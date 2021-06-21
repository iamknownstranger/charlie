from kiteconnect import ticker
from talib import RSI, WMA
import talib
import numpy as np
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime, timedelta
import csv
from pandas.tseries.offsets import BDay

print("Om Namahshivaya:")


today = datetime.today()
previous_trading_day = (datetime.today() - BDay(1)).strftime("%Y-%m-%d")

kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


nse = pd.read_csv("/workspaces/charlie/NSEBSE/equity_nse.csv")
bse = pd.read_csv("/workspaces/charlie/NSEBSE/equity_bse.csv")

bse_instruments = pd.DataFrame(kite.instruments("BSE"))
nse_instruments = pd.DataFrame(kite.instruments("NSE"))

merged = pd.merge(left=nse, right=bse, left_on=' ISIN NUMBER', right_on='ISIN No', how='inner')
print(merged.columns)
listed = merged[['NAME OF COMPANY', 'SYMBOL', 'Security Id']]
print(listed.columns)

# listed.set_axis(['index', 'name', 'nse_symbol, bse_symbol'], axis='columns', inplace=True)
# listed.columns = ['name', 'nse_symbol, bse_symbol']
listed.columns=['name', 'nse_symbol', 'bse_symbol']
print(listed.columns)
# merged[['NAME OF COMPANY', 'SYMBOL', 'Security Id']].to_csv(
    # "/workspaces/charlie/NSEBSE/tradingsymbols_listed_on_both.csv", index=False)

tickers = {}

for index, row in listed.iterrows():
    try:
        nse_instrument_token = nse_instruments.loc[nse_instruments.tradingsymbol ==
                                                row['nse_symbol']].values[0][0]
        bse_instrument_token = bse_instruments.loc[bse_instruments.tradingsymbol == row['bse_symbol']].values[0][0]
        tickers[row['name']] = {'nse_token':nse_instrument_token, 'bse_token':bse_instrument_token}
        # print(tickers)
    except:
        print(row)
        continue
    # break

print(tickers)
# # print(nse.head())

# # print(bse.head())

# symbols = merged[["Security Id", "SYMBOL"]]
# symbols.to_csv("bse_nse_symbols.csv", index=False)

# print(merged.to_csv("both_exchanges.csv", index = False))

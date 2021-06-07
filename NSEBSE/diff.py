import pandas as pd
nse = pd.read_csv("/home/ubuntu/charlie/NSEBSE/equity_bse.csv")
bse = pd.read_csv("/home/ubuntu/charlie/NSEBSE/equity_nse.csv")
# print(nse.columns, bse.columns)

bse.columns = ['SYMBOL', 'NAME OF COMPANY', ' SERIES', ' DATE OF LISTING', ' PAID UP VALUE', ' MARKET LOT', 'ISIN No', ' FACE VALUE']

merged = pd.merge(nse, bse, on='ISIN No')
# print(nse.head())
# print(bse.head())
symbols = merged[["Security Id", "SYMBOL"]]
symbols.to_csv("bse_nse_symbols.csv", index=False)

print(merged.to_csv("both_exchanges.csv", index = False))

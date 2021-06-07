from jugaad_trader import Zerodha

import pandas as pd


kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

nse_df = pd.DataFrame(kite.instruments("NSE"))
bse_df = pd.DataFrame(kite.instruments("BSE"))
bse_df.drop_duplicates("")
filter1 = bse_df["lot_size"]== 1
filter2 = bse_df["instrument_type"]=="EQ"
filter3 = bse_df["tick_size"] == 0.05
bse_df = bse_df.where(filter1 & filter2 & filter3)
common = pd.merge(nse_df, bse_df, on="name")
print(common)

common.to_csv("common.csv")

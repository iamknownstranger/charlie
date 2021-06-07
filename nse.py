from jugaad_trader import Zerodha

import pandas as pd


kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

bse_df = pd.DataFrame(kite.instruments("BSE"))
print(bse_df.columns)
filter1 = bse_df["lot_size"]==1
filter2 = bse_df["instrument_type"]=="EQ"
bse_df = bse_df.where(filter1 & filter2)

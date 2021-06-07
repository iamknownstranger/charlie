from jugaad_trader import Zerodha

import pandas as pd


kite = Zerodha()


# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

nse_df = pd.DataFrame(kite.instruments("NSE"))
bse_df = pd.DataFrame(kite.instruments("BSE"))
common = pd.merge(nse_df, bse_df, on="name")

common.to_csv("common.csv")

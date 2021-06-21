from jugaad_trader import Zerodha

import csv

print("Om Namahshivaya:")



kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

instruments = pd.read_csv("/workspaces/charlie/NSEBSE/tradingsymbols_listed_on_both.csv")

for index, row in instruments.iterrows():
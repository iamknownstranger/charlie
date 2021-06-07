# import pandas as pd
# df = pd.read_csv("symbols.csv")
# dropna = df.dropna()
# dropna.to_csv("symbols.csv", index= False)

from jugaad_trader import Zerodha

import csv

print("Om Namahshivaya:")



kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()

watchlist = []



with open("symbols.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # print(row['nse_token'])
        if(row['nse_token'] == "" or row['bse_token'] == ""):
            continue
        ltp_nse = kite.ltp(row['nse_token'])[row['nse_token']]['last_price']
        ltp_bse = kite.ltp(row['bse_token'])[row['bse_token']]['last_price']

        if(ltp_nse == ltp_nse):
            print("=", end="")
            continue
        elif(ltp_nse > ltp_bse):
            print("LTP is higher in NSE is greater than that in BSE")


        else:
            print("LTP is higher in BSE is greater than that in NSE")
        print("Difference: ", ltp_nse - ltp_bse, ltp_nse, ltp_bse)

        watchlist.append((row['nse_token'], row['bse_token']))

print("watchlist", watchlist)
tradebook = open("tradebook.txt", "w")
for nse_token, bse_token in watchlist:
    ltp_nse = kite.ltp(nse_token)[nse_token]['last_price']
    ltp_bse = kite.ltp(bse_token)[bse_token]['last_price']
    tradebook.write("\n" + nse_token + " nse ltp " +
                        str(ltp_nse) + bse_token + " bse ltp " + str(ltp_bse))
    






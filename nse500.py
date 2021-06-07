import csv
import numpy as np
import pandas as pd
from datetime import datetime
from pprint import pprint
import datetime as dt
import pytz
from jugaad_trader import Zerodha
import talib
from ta import add_all_ta_features

nse500 = ['3MINDIA', 'ABB', 'POWERINDIA', 'ACC', 'AIAENG', 'APLAPOLLO', 'AUBANK', 'AARTIDRUGS', 'AARTIIND', 'AAVAS', 'ABBOTINDIA', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ATGL', 'ADANITRANS', 'ABCAPITAL', 'ABFRL', 'ADVENZYMES', 'AEGISCHEM', 'AFFLE', 'AJANTPHARM', 'AKZOINDIA', 'ALEMBICLTD', 'APLLTD', 'ALKEM', 'ALKYLAMINE', 'ALOKINDS', 'AMARAJABAT', 'AMBER', 'AMBUJACEM', 'ANGELBRKG', 'APOLLOHOSP', 'APOLLOTYRE', 'ASAHIINDIA', 'ASHOKLEY', 'ASHOKA', 'ASIANPAINT', 'ASTERDM', 'ASTRAZEN', 'ASTRAL', 'ATUL', 'AUROPHARMA', 'AVANTIFEED', 'DMART', 'AXISBANK', 'BASF', 'BEML', 'BSE', 'BAJAJ-AUTO', 'BAJAJCON', 'BAJAJELEC', 'BAJFINANCE', 'BAJAJFINSV', 'BAJAJHLDNG', 'BALAMINES', 'BALKRISIND', 'BALMLAWRIE', 'BALRAMCHIN', 'BANDHANBNK', 'BANKBARODA', 'BANKINDIA', 'MAHABANK', 'BATAINDIA', 'BAYERCROP', 'BERGEPAINT', 'BDL', 'BEL', 'BHARATFORG', 'BHEL', 'BPCL', 'BHARATRAS', 'BHARTIARTL', 'BIOCON', 'BIRLACORPN', 'BSOFT', 'BLISSGVS', 'BLUEDART', 'BLUESTARCO', 'BBTC', 'BOSCHLTD', 'BRIGADE', 'BRITANNIA', 'BURGERKING', 'CCL', 'CESC', 'CRISIL', 'CSBBANK', 'CADILAHC', 'CANFINHOME', 'CANBK', 'CAPLIPOINT', 'CGCL', 'CARBORUNIV', 'CASTROLIND', 'CEATLTD', 'CENTRALBK', 'CDSL', 'CENTURYPLY', 'CENTURYTEX', 'CERA', 'CHALET', 'CHAMBLFERT', 'CHOLAHLDNG', 'CHOLAFIN', 'CIPLA', 'CUB', 'COALINDIA', 'COCHINSHIP', 'COFORGE', 'COLPAL', 'CAMS', 'CONCOR', 'COROMANDEL', 'CREDITACC', 'CROMPTON', 'CUMMINSIND', 'CYIENT', 'DCBBANK', 'DCMSHRIRAM', 'DLF', 'DABUR', 'DALBHARAT', 'DEEPAKNTR', 'DELTACORP', 'DHANI', 'DHANUKA', 'DBL', 'DISHTV', 'DCAL', 'DIVISLAB', 'DIXON', 'LALPATHLAB', 'DRREDDY', 'EIDPARRY', 'EIHOTEL', 'EPL', 'EDELWEISS', 'EICHERMOT', 'ELGIEQUIP', 'EMAMILTD', 'ENDURANCE', 'ENGINERSIN', 'EQUITAS', 'ERIS', 'ESCORTS', 'EXIDEIND', 'FDC', 'FEDERALBNK', 'FINEORG', 'FINCABLES', 'FINPIPE', 'FSL', 'FORTIS', 'FCONSUMER', 'FRETAIL', 'GAIL', 'GEPIL', 'GMMPFAUDLR', 'GMRINFRA', 'GALAXYSURF', 'GRSE', 'GARFIBRES', 'GICRE', 'GILLETTE', 'GLAXO', 'GLENMARK', 'GODFRYPHLP', 'GODREJAGRO', 'GODREJCP', 'GODREJIND', 'GODREJPROP', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GESHIP', 'GREAVESCOT', 'GRINDWELL', 'GUJALKALI', 'GAEL', 'FLUOROCHEM', 'GUJGASLTD', 'GNFC', 'GPPL', 'GSFC', 'GSPL', 'GULFOILLUB', 'HEG', 'HCLTECH', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HFCL', 'HAPPSTMNDS', 'HATSUN', 'HAVELLS', 'HEIDELBERG', 'HEMIPROP', 'HEROMOTOCO', 'HSCL', 'HINDALCO', 'HAL', 'HINDCOPPER', 'HINDPETRO', 'HINDUNILVR', 'HINDZINC', 'HONAUT', 'HUDCO', 'HDFC', 'HUHTAMAKI', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'ISEC', 'IDBI', 'IDFCFIRSTB', 'IDFC', 'IFBIND', 'IIFL', 'IIFLWAM', 'IOLCP', 'IRB', 'IRCON', 'ITC', 'ITI', 'INDIACEM', 'IBULHSGFIN', 'IBREALEST', 'INDIAMART', 'INDIANB', 'IEX', 'INDHOTEL', 'IOC', 'IOB', 'IRCTC', 'ICIL', 'INDOCO', 'IGL', 'INDUSTOWER', 'INDUSINDBK', 'INFIBEAM', 'NAUKRI', 'INFY', 'INGERRAND', 'INOXLEISUR', 'INTELLECT', 'INDIGO', 'IPCALAB',
    'JBCHEPHARM', 'JKCEMENT', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JMFINANCIL', 'JSWENERGY', 'JSWSTEEL', 'JTEKTINDIA', 'JAMNAAUTO', 'JINDALSAW', 'JSLHISAR', 'JSL', 'JINDALSTEL', 'JCHAC', 'JUBLFOOD', 'JUSTDIAL', 'JYOTHYLAB', 'KPRMILL', 'KEI', 'KNRCON', 'KPITTECH', 'KRBL', 'KSB', 'KAJARIACER', 'KALPATPOWR', 'KANSAINER', 'KARURVYSYA', 'KSCL', 'KEC', 'KOTAKBANK', 'L&TFH', 'LTTS', 'LICHSGFIN', 'LAOPALA', 'LAXMIMACH', 'LTI', 'LT', 'LAURUSLABS', 'LEMONTREE', 'LINDEINDIA', 'LUPIN', 'LUXIND', 'MASFIN', 'MMTC', 'MOIL', 'MRF', 'MGL', 'MAHSCOOTER', 'MAHSEAMLES', 'M&MFIN', 'M&M', 'MAHINDCIE', 'MHRIL', 'MAHLOG', 'MANAPPURAM', 'MRPL', 'MARICO', 'MARUTI', 'MFSL', 'MAXHEALTH', 'MAZDOCK', 'METROPOLIS', 'MINDTREE', 'MINDACORP', 'MINDAIND', 'MIDHANI', 'MOTHERSUMI', 'MOTILALOFS', 'MPHASIS', 'MCX', 'MUTHOOTFIN', 'NATCOPHARM', 'NBCC', 'NCC', 'NESCO', 'NHPC', 'NLCINDIA', 'NMDC', 'NOCIL', 'NTPC', 'NH', 'NATIONALUM', 'NFL', 'NAVINFLUOR', 'NESTLEIND', 'NETWORK18', 'NILKAMAL', 'NAM-INDIA', 'OBEROIRLTY', 'ONGC', 'OIL', 'OFSS', 'ORIENTELEC', 'ORIENTREF', 'PIIND', 'PNBHOUSING', 'PNCINFRA', 'PVR', 'PAGEIND', 'PERSISTENT', 'PETRONET', 'PFIZER', 'PHILIPCARB', 'PHOENIXLTD', 'PIDILITIND', 'PEL', 'POLYMED', 'POLYCAB', 'POLYPLEX', 'PFC', 'POWERGRID', 'PRESTIGE', 'PRINCEPIPE', 'PRSMJOHNSN', 'PGHL', 'PGHH', 'PNB', 'QUESS', 'RBLBANK', 'RECLTD', 'RITES', 'RADICO', 'RVNL', 'RAIN', 'RAJESHEXPO', 'RALLIS', 'RCF', 'RATNAMANI', 'RAYMOND', 'REDINGTON', 'RELAXO', 'RELIANCE', 'RESPONIND', 'ROSSARI', 'ROUTE', 'SBICARD', 'SBILIFE', 'SIS', 'SJVN', 'SKFINDIA', 'SRF', 'SANOFI', 'SCHAEFFLER', 'SCHNEIDER', 'SEQUENT', 'SHARDACROP', 'SFL', 'SHILPAMED', 'SCI', 'SHOPERSTOP', 'SHREECEM', 'SHRIRAMCIT', 'SRTRANSFIN', 'SIEMENS', 'SOBHA', 'SOLARINDS', 'SOLARA', 'SONATSOFTW', 'SPANDANA', 'SPICEJET', 'STARCEMENT', 'SBIN', 'SAIL', 'SWSOLAR', 'STLTECH', 'STAR', 'SUDARSCHEM', 'SUMICHEM', 'SPARC', 'SUNPHARMA', 'SUNTV', 'SUNCLAYLTD', 'SUNDARMFIN', 'SUNDRMFAST', 'SUNTECK', 'SUPRAJIT', 'SUPREMEIND', 'SUPPETRO', 'SUVENPHAR', 'SUZLON', 'SWANENERGY', 'SYMPHONY', 'SYNGENE', 'TCIEXP', 'TCNSBRANDS', 'TTKPRESTIG', 'TV18BRDCST', 'TVSMOTOR', 'TANLA', 'TASTYBITE', 'TATACHEM', 'TATACOFFEE', 'TATACOMM', 'TCS', 'TATACONSUM', 'TATAELXSI', 'TATAINVEST', 'TATAMTRDVR', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TEAMLEASE', 'TECHM', 'NIACL', 'RAMCOCEM', 'THERMAX', 'THYROCARE', 'TIMKEN', 'TITAN', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TRIDENT', 'TRITURBINE', 'TIINDIA', 'UCOBANK', 'UFLEX', 'UPL', 'UTIAMC', 'UJJIVAN', 'UJJIVANSFB', 'ULTRACEMCO', 'UNIONBANK', 'UBL', 'MCDOWELL-N', 'VGUARD', 'VMART', 'VIPIND', 'VSTIND', 'VAIBHAVGBL', 'VAKRANGEE', 'VALIANTORG', 'VTL', 'VARROC', 'VBL', 'VEDL', 'VENKEYS', 'VINATIORGA', 'IDEA', 'VOLTAS', 'WABCOINDIA', 'WELCORP', 'WELSPUNIND', 'WESTLIFE', 'WHIRLPOOL', 'WIPRO', 'WOCKPHARMA', 'YESBANK', 'ZEEL', 'ZENSARTECH', 'ZYDUSWELL', 'ECLERX']


# from mpl_finance import candlestick_ohlc
# import matplotlib.pyplot as plt

# from candle import Candle

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime("%Y:%m:%d %H:%M:%S")


kite = Zerodha()

kite.set_access_token()


nse_instruments = pd.DataFrame(kite.instruments("NSE"))
nse500_instruments = nse_instruments.loc[nse_instruments.tradingsymbol.isin(
    nse500)]
watchlist = nse500_instruments.instrument_token.tolist()

touchdown = open("ema21touchdown5min.csv", "w")

for stock in watchlist:
    tick_data = pd.DataFrame(kite.historical_data(
        stock, "2021-04-01 09:15:00", "2021-05-31 03:30:00", "5minute"))
    
    # tick_data.set_index(pd.DatetimeIndex(tick_data["date"]), inplace=True)
    data = tick_data.tail(21)
    period_high = data.high.max()
    period_low = data.low.min()
    today_data = kite.quote(stock)[str(stock)]
    today_high = today_data['ohlc']['high']
    today_low = today_data['ohlc']['low']
    today_close = today_data['last_price']
    # data = add_all_ta_features(tick_data, open="open", high="high", low="low", close="close", volume="volume")
    # print(data.to_csv("allfeatures.csv"))
    # print("\n" + stock)
    # if(today_high >= period_high):
    #     print("21 day High Breakout")
    # elif (today_low <= period_low):
    #     print("21 day Low Breakdown")
    # if(last_price > period_high):
    #     print("Closed above 21 day High")

    
    ema21 = talib.EMA(data['close'].to_numpy(), timeperiod=21)[-1]
    if(ema21 >= today_low):
        if(ema21 <= today_close):
            touchdown.write("\n Touchdown," + str(stock))
    
  

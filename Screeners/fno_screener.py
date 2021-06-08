import talib
from pandas.tseries.offsets import BDay
from pprint import pprint
from jugaad_trader import Zerodha
import pandas as pd
import pytz
from datetime import datetime, timedelta, date
import csv
from ta.volume import volume_weighted_average_price


print('Om Namahshivaya:')

# get the standard UTC time
UTC = pytz.utc

# it will get the time zone
# of the specified location
IST = pytz.timezone('Asia/Kolkata')


def get_timestamp():
    return datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')


previous_trading_day = (datetime.today() - BDay(1)).strftime('%Y-%m-%d')


def get_ltp(instrument_token):
    return kite.ltp(instrument_token)[str(instrument_token)]['last_price']


def buy(instrument_token):
    if instrument_token not in open_trades:
        buy_price = get_ltp(instrument_token)
        orderbook.write("Bought " + ticker_dictionary.get(instrument_token,
                        'No Key Found')['name'] + " at " + str(buy_price))
        open_trades.append(instrument_token)


def sell(instrument_token):
    if instrument_token in open_trades:
        sell_price = get_ltp(instrument_token)
        orderbook.write("Sold " + ticker_dictionary.get(instrument_token,
                        'No Key Found')['name'] + " at " + str(sell_price))
        open_trades.remove(instrument_token)


def get_historical_data(instrument, inception_date, interval):
    """extracts historical data and outputs in the form of dataframe
       inception date string format - dd-mm-yyyy"""
    from_date = datetime.strptime(inception_date, '%d-%m-%Y')
    to_date = date.today()
    data = pd.DataFrame(
        columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    while True:
        if from_date.date() >= (date.today() - timedelta(100)):
            data = data.append(pd.DataFrame(kite.historical_data(
                instrument, from_date, date.today(), interval)), ignore_index=True)
            break
        else:
            to_date = from_date + timedelta(100)
            data = data.append(pd.DataFrame(kite.historical_data(
                instrument, from_date, to_date, interval)), ignore_index=True)
            from_date = to_date
    data.set_index("date", inplace=True)
    return data


kite = Zerodha()

# Set access token loads the stored session.
# Name chosen to keep it compatible with kiteconnect.
kite.set_access_token()


fno_stocks = {1793: 'AARTIIND', 5633: 'ACC', 6401: 'ADANIENT', 3861249: 'ADANIPORTS', 25601: 'AMARAJABAT', 325121: 'AMBUJACEM', 40193: 'APOLLOHOSP', 41729: 'APOLLOTYRE', 54273: 'ASHOKLEY', 60417: 'ASIANPAINT', 70401: 'AUROPHARMA', 1510401: 'AXISBANK', 4267265: 'BAJAJ-AUTO', 81153: 'BAJFINANCE', 4268801: 'BAJAJFINSV', 85761: 'BALKRISIND', 579329: 'BANDHANBNK', 1195009: 'BANKBARODA', 94977: 'BATAINDIA', 103425: 'BERGEPAINT', 98049: 'BEL', 108033: 'BHARATFORG', 112129: 'BHEL', 134657: 'BPCL', 2714625: 'BHARTIARTL', 2911489: 'BIOCON', 558337: 'BOSCHLTD', 140033: 'BRITANNIA', 2029825: 'CADILAHC', 2763265: 'CANBK', 175361: 'CHOLAFIN', 177665: 'CIPLA', 5215745: 'COALINDIA', 2955009: 'COFORGE', 3876097: 'COLPAL', 1215745: 'CONCOR', 486657: 'CUMMINSIND', 197633: 'DABUR', 2800641: 'DIVISLAB', 3771393: 'DLF', 2983425: 'LALPATHLAB', 225537: 'DRREDDY', 232961: 'EICHERMOT', 245249: 'ESCORTS', 173057: 'EXIDEIND', 1207553: 'GAIL', 1895937: 'GLENMARK', 3463169: 'GMRINFRA', 2585345: 'GODREJCP', 4576001: 'GODREJPROP', 315393: 'GRASIM', 2513665: 'HAVELLS', 1850625: 'HCLTECH', 1086465: 'HDFCAMC', 341249: 'HDFCBANK', 119553: 'HDFCLIFE', 345089: 'HEROMOTOCO', 348929: 'HINDALCO', 359937: 'HINDPETRO', 356865: 'HINDUNILVR', 340481: 'HDFC', 1270529: 'ICICIBANK', 5573121: 'ICICIGI', 4774913: 'ICICIPRULI', 2863105: 'IDFCFIRSTB', 7712001: 'IBULHSGFIN', 415745: 'IOC', 2883073: 'IGL', 7458561: 'INDUSTOWER', 1346049: 'INDUSINDBK', 3520257: 'NAUKRI', 408065: 'INFY', 2865921: 'INDIGO', 424961: 'ITC', 1723649: 'JINDALSTEL', 3001089: 'JSWSTEEL', 4632577: 'JUBLFOOD', 492033: 'KOTAKBANK', 6386689: 'L&TFH', 2939649: 'LT', 511233: 'LICHSGFIN', 2672641: 'LUPIN', 4488705: 'MGL', 3400961: 'M&MFIN', 519937: 'M&M', 4879617: 'MANAPPURAM', 1041153: 'MARICO', 2815745: 'MARUTI', 548353: 'MFSL', 3675137: 'MINDTREE', 1076225: 'MOTHERSUMI', 582913: 'MRF', 6054401: 'MUTHOOTFIN', 1629185: 'NATIONALUM', 4598529: 'NESTLEIND', 3924993: 'NMDC', 2977281: 'NTPC', 633601: 'ONGC', 3689729: 'PAGEIND', 2905857: 'PETRONET', 681985: 'PIDILITIND', 617473: 'PEL', 3660545: 'PFC', 3834113: 'POWERGRID', 2730497: 'PNB', 3365633: 'PVR', 4708097: 'RBLBANK', 3930881: 'RECLTD', 738561: 'RELIANCE', 5582849: 'SBILIFE', 794369: 'SHREECEM', 1102337: 'SRTRANSFIN', 806401: 'SIEMENS', 837889: 'SRF', 779521: 'SBIN', 758529: 'SAIL', 857857: 'SUNPHARMA', 3431425: 'SUNTV', 871681: 'TATACHEM', 2953217: 'TCS', 878593: 'TATACONSUM', 884737: 'TATAMOTORS', 877057: 'TATAPOWER', 895745: 'TATASTEEL', 3465729: 'TECHM', 261889: 'FEDERALBNK', 523009: 'RAMCOCEM', 897537: 'TITAN', 900609: 'TORNTPHARM', 3529217: 'TORNTPOWER', 2170625: 'TVSMOTOR', 2952193: 'ULTRACEMCO', 4278529: 'UBL', 2674433: 'MCDOWELL-N', 2889473: 'UPL', 784129: 'VEDL', 3677697: 'IDEA', 951809: 'VOLTAS', 969473: 'WIPRO', 975873: 'ZEEL', 2995969: 'ALKEM', 5436929: 'AUBANK', 5105409: 'DEEPAKNTR', 3484417: 'IRCTC', 91393: 'NAM-INDIA', 4561409: 'LTI', 3756033: 'NAVINFLUOR', 676609: 'PFIZER', 6191105: 'PIIND', 502785: 'TRENT', 6483969: 'APLLTD', 1459457: 'CUB', 3039233: 'GRANULES', 2713345: 'GUJGASLTD', 4752385: 'LTTS', 1152769: 'MPHASIS'}
screener = open("/home/ubuntu/charlie/Screeners/screener_output.txt", "w")

# intervals = {'minute':21, '3minute':61, '5minute':61, '10minute':61,
#              '15minute':144, '30minute':144, '60minute':210, 'day':365}

intervals = {'60minute':210, 'day':365}

for instrument_token, symbol in fno_stocks.items():
    for interval, limit in intervals.items():
        candle_data = pd.DataFrame(kite.historical_data(
            instrument_token, date.today()-timedelta(days=limit), datetime.today(), interval))
        candle_data['ema21'] = talib.EMA(candle_data.close, timeperiod=21)
        candle_data['ema210'] = talib.EMA(candle_data.close, timeperiod=210)
        candle_data['vwap21'] = volume_weighted_average_price(
            high=candle_data.high, low=candle_data.low, close=candle_data.close, volume=candle_data.volume, window=21)
        candle_data['vwap210'] = volume_weighted_average_price(
            high=candle_data.high, low=candle_data.low, close=candle_data.close, volume=candle_data.volume, window=210)
        candle_data["rsi21"] = talib.RSI(candle_data.close, timeperiod=21)
        candle_data["rsi34"] = talib.RSI(candle_data.close, timeperiod=34)
        candle_data["rsi210"] = talib.RSI(candle_data.close, timeperiod=210)
        
        penultimate_candle = candle_data.iloc[-2]
        last_candle = candle_data.iloc[-1]

        if penultimate_candle.rsi34 > 66:
            if last_candle.close <= 66:
                screener.write("\n" + symbol + " Touched at 66 - 34 period RSI, interval:" + str(interval))
                print(symbol, "Touched at 34 period RSI, interval:", interval)

        if penultimate_candle.rsi21 > 66:
            if last_candle.close <= 66:
                screener.write("\n" + symbol + " Touched at 79 - 21 period RSI, interval:" + str(interval))
                print(symbol, "Tookoff at 21 period RSI, interval:", interval)

        if penultimate_candle.rsi21 > 79:
            if last_candle.close <= 79:
                screener.write("\n" + symbol + " Tookoff at 79 - 21 period RSI, interval:" + str(interval))
                print(symbol, "Tookoff at 21 period RSI, interval:", interval)
        

        if penultimate_candle.rsi34 < 34:
            if last_candle.close >= 34:
                screener.write("\n" + symbol + " Tookoff at 34 - 34 period RSI, interval:" + str(interval))
                print(symbol, "Tookoff at 34 period RSI, interval:", interval)

        if penultimate_candle.rsi21 < 34:
            if last_candle.close >= 34:
                screener.write("\n" + symbol + " Tookoff at 34 - 21 period RSI, interval:" + str(interval))
                print(symbol, "Tookoff at 34 period RSI, interval:", interval)
        
        if penultimate_candle.rsi21 < 21:
            if last_candle.close >= 21:
                screener.write("\n" + symbol + " Tookoff at 21 - 21 period RSI, interval:" + str(interval))
                print(symbol, "Tookoff at 21 period RSI, interval:", interval)
    

        if last_candle.low <= penultimate_candle.ema21:
            if last_candle.close >= penultimate_candle.ema21:
                screener.write("\n" + symbol + " Support at 21 period EMA interval:" + str(interval))
                print(symbol, "Support at 21 period EMA interval:", interval)

        if last_candle.low <= penultimate_candle.ema210:
            if last_candle.close >= penultimate_candle.ema210:
                screener.write("\n" + symbol + " Support at 21 period EMA interval:" + str(interval))
                print(symbol, "Support at 210 period EMA interval:", interval)

        if last_candle.low <= penultimate_candle.vwap21:
            if last_candle.close >= penultimate_candle.vwap21:
                screener.write("\n" + symbol +  " Support at 210 VWAP interval:" + str(interval))
                print(symbol, "Support at 21 period VWAP interval:", interval)

        if last_candle.low <= penultimate_candle.vwap210:
            if last_candle.close >= penultimate_candle.vwap210:
                screener.write("\n" + symbol +  " Support at 210 period VWAP interval:" + str(interval))
                print(symbol, "Support at 210 period VWAP interval:", interval)


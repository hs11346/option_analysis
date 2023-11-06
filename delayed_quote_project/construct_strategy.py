import pandas as pd
import numpy as np
import warnings
import yfinance as yf
from opx_chain import options_chain
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
def underlying_vol(ticker, days=60):
    df = yf.download(ticker, interval='1d',period = '1y')
    df['Ret'] = (df['Adj Close'] / df['Adj Close'].shift(1))
    df['Volatility'] = df['Ret'].rolling(window=days).std() # unannualised
    return df.Volatility.iloc[-1]
def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1mo', interval = '1d')
    return todays_data['Close'][-1]
def PCS_screener(list_,IsITM = False, moneyness = 0.8, max_strike_width = 4, min_dte = 0, max_dte = 30, fees = 0.1, min_dist = 0, min_bid = 0):
    x = []
    for i in list_:
        results = put_credit_spread(i, IsITM = IsITM, moneyness = moneyness, max_strike_width = max_strike_width, min_dte = min_dte, max_dte = max_dte, fees = fees, min_dist = min_dist, min_bid = min_bid)
        print("{} combinations found".format(len(results)))
        if results.empty == False:
            x.append(results)
        else:
            pass
    try:
        df = pd.concat(x)
        return df
    except ValueError:
        pass

def CCS_screener(list_,IsITM = False, moneyness = 1.2, max_strike_width = 4, min_dte = 0, max_dte = 30, fees = 0.1, min_dist = 0, min_bid = 0):
    x = []
    for i in list_:
        results = call_credit_spread(i, IsITM = IsITM, moneyness = moneyness, max_strike_width = max_strike_width, min_dte = min_dte, max_dte = max_dte, fees = fees, min_dist = min_dist, min_bid = min_bid)
        print("{} combinations found".format(len(results)))
        if results.empty == False:
            x.append(results)
        else:
            pass
    try:
        df = pd.concat(x)
        return df
    except ValueError:
        pass
def put_credit_spread(underlying, IsITM = False, moneyness = 0.8, max_strike_width = 4, min_dte = 0, max_dte = 30, fees = 0.1, min_dist = 0, min_bid = 0):
    # PCS -> Short higher strike, long lower strike; Fee structure based on two way fees, futu fees = $10 per contract ($0.1)
    # Moneyness is the minimum moneyness of option strikes for scanning
    print("Start combination for " + underlying + " Put Credit Spread")
    current_price = get_current_price(underlying)
    df = options_chain(underlying)
    df = df[df.ITM == IsITM][df.CPFlag == False][(df.bid >= 0)|(df.ask >=0)][df.strike >= current_price*moneyness] # Extract OTM Puts from chain with non-zero bid-ask
    spread_df = pd.DataFrame()
    df.reset_index(inplace=True, drop=True)
    for short_index in df.index.to_list(): # Loop for all combinations of put vertical spreads
        for long_index in df.index.to_list():
            if abs(df.iloc[short_index].strike - df.iloc[long_index].strike) <= max_strike_width and \
                    df.iloc[short_index].exDate == df.iloc[long_index].exDate and \
                    df.iloc[short_index].strike > df.iloc[long_index].strike and \
                    df.iloc[short_index].dte <= max_dte and df.iloc[short_index].dte >= min_dte: # Specify maximum strike width and same exDate
                dict_ = {"symbol":df.iloc[long_index].symbol+"-"+df.iloc[short_index].symbol\
                                    ,"width":df.iloc[short_index].strike - df.iloc[long_index].strike,
                         "short_strike":df.iloc[short_index].strike, "long_strike":df.iloc[long_index].strike,\
                         "bid":df.iloc[short_index].bid-df.iloc[long_index].ask,\
                                  "ask":df.iloc[short_index].ask-df.iloc[long_index].bid,\
                                  'min_vol':min(df.iloc[short_index].volume,df.iloc[long_index].volume),\
                                  'min_oi':min(df.iloc[short_index].OI,df.iloc[long_index].OI),\
                                  'exDate':df.iloc[short_index].exDate,\
                                  'dte':df.iloc[short_index].dte}
                spread_df = pd.concat([spread_df,pd.DataFrame(dict_, index = [0])], ignore_index=True)
    print("All combinations scanned")
    if spread_df.empty:
        return spread_df
    # Risk-reward ratio, Reward adjusted down by fees
    spread_df['RR_ratio'] = ((spread_df.bid + spread_df.ask - fees * 2) / (2 * spread_df.width))*100
    spread_df = spread_df[spread_df['RR_ratio'] > 0]
    #ATM distance is the % difference between strike and underlying price divided by the return volatility (adjusted by dte)
    spread_df['ATM_dist'] = (abs(spread_df['short_strike'] - current_price)/current_price)/(underlying_vol(underlying, days=60) * np.sqrt(spread_df.dte + 1))
    spread_df = spread_df[spread_df.ATM_dist >= min_dist]
    # Min bid
    spread_df = spread_df[spread_df.bid >= min_bid]
    # RR_ratio / ATM_dist
    spread_df['dist_RR'] = spread_df.ATM_dist/spread_df.RR_ratio
    spread_df[['min_vol', 'min_oi']] = spread_df[['min_vol', 'min_oi']].astype(int)
    spread_df = spread_df.sort_values(by='dist_RR', ascending=False)
    print("{} combinations found".format(len(spread_df)))
    return spread_df.round(2)

def call_credit_spread(underlying, IsITM = False, moneyness = 1.2, max_strike_width = 4, min_dte = 0, max_dte = 30, fees = 0.1, min_dist = 0, min_bid = 0):
    # CCS -> long higher strike, short lower strike; Fee structure based on two way fees, futu fees = $10 per contract ($0.1)
    # Moneyness is the minimum moneyness of option strikes for scanning
    print("Start combination for " + underlying + " Call Credit Spread")
    current_price = get_current_price(underlying)
    df = options_chain(underlying)
    df = df[df.ITM == IsITM][df.CPFlag == True][(df.bid >= 0)|(df.ask >=0)][df.strike <= current_price*moneyness] # Extract OTM Puts from chain with non-zero bid-ask
    spread_df = pd.DataFrame()
    df.reset_index(inplace=True, drop=True)
    for short_index in df.index.to_list(): # Loop for all combinations of put vertical spreads
        for long_index in df.index.to_list():
            if abs(df.iloc[short_index].strike - df.iloc[long_index].strike) <= max_strike_width and \
                    df.iloc[short_index].exDate == df.iloc[long_index].exDate and \
                    df.iloc[short_index].strike < df.iloc[long_index].strike and \
                    df.iloc[short_index].dte <= max_dte and df.iloc[short_index].dte >= min_dte: # Specify maximum strike width and same exDate
                dict_ = {"symbol":df.iloc[long_index].symbol+"-"+df.iloc[short_index].symbol\
                                    ,"width":df.iloc[long_index].strike - df.iloc[short_index].strike,
                         "short_strike":df.iloc[short_index].strike, "long_strike":df.iloc[long_index].strike,\
                         "bid":df.iloc[short_index].bid-df.iloc[long_index].ask,\
                                  "ask":df.iloc[short_index].ask-df.iloc[long_index].bid,\
                                  'min_vol':min(df.iloc[short_index].volume,df.iloc[long_index].volume),\
                                  'min_oi':min(df.iloc[short_index].OI,df.iloc[long_index].OI),\
                                  'exDate':df.iloc[short_index].exDate,\
                                  'dte':df.iloc[short_index].dte}
                spread_df = pd.concat([spread_df,pd.DataFrame(dict_, index = [0])], ignore_index=True)
    print("All combinations scanned")
    if spread_df.empty:
        return spread_df
    # Risk-reward ratio, Reward adjusted down by fees
    spread_df['RR_ratio'] = ((spread_df.bid + spread_df.ask - fees * 2) / (2 * spread_df.width))*100
    spread_df = spread_df[spread_df['RR_ratio'] > 0]
    #ATM distance is the % difference between strike and underlying price divided by the return volatility (adjusted by dte)
    spread_df['ATM_dist'] = (abs(spread_df['short_strike'] - current_price)/current_price)/(underlying_vol(underlying, days=60) * np.sqrt(spread_df.dte + 1))
    spread_df = spread_df[spread_df.ATM_dist >= min_dist]
    # Min bid
    spread_df = spread_df[spread_df.bid >= min_bid]
    # RR_ratio / ATM_dist
    spread_df['dist_RR'] = spread_df.ATM_dist/spread_df.RR_ratio
    spread_df.fillna(0,inplace=True)
    spread_df[['min_vol', 'min_oi']] = spread_df[['min_vol', 'min_oi']].astype(int)
    spread_df = spread_df.sort_values(by='dist_RR', ascending=False)
    print("{} combinations found".format(len(spread_df)))
    return spread_df.round(2)

def rsi_value(underlying, upper = 70, lower = 30):
    symbol = yf.Ticker(underlying)
    df = symbol.history(interval="1d", period="1mo").tail(30)
    change = df["Close"].diff()
    change.dropna(inplace=True)
    # Create two copies of the Closing price Series
    change_up = change.copy()
    change_down = change.copy()
    change_up[change_up < 0] = 0
    change_down[change_down > 0] = 0
    change.equals(change_up + change_down)
    avg_up = change_up.rolling(14).mean()
    avg_down = change_down.rolling(14).mean().abs()
    rsi = 100 * avg_up / (avg_up + avg_down)
    # Take a look at the 20 oldest datapoints
    value = rsi.iloc[-1]
    if value >= upper:
        value = 1
    elif value <= lower:
        value = -1
    else:
        value = 0
    return value

def RSI_screener(df, upper = 70, lower = 30):
    df['rsi'] = df.Tickers.apply(lambda x: rsi_value(x, upper = upper, lower= lower))
    return df[df.rsi != 0]


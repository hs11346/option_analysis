import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import pandas_market_calendars as mcal
nyse = mcal.get_calendar('NYSE')
holidays = nyse.holidays()
holidays = list(holidays.holidays)
def options_chain(symbol):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        #opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt = pd.concat([pd.DataFrame(),pd.DataFrame(opt.calls),pd.DataFrame(opt.puts)], ignore_index=True)
        opt['expirationDate'] = e
        options = pd.concat([options,pd.DataFrame(opt)], ignore_index=True)

    # Bizarre error in yfinance that gives the wrong expiration date (RESOLVED)
    # Add 1 day to get the correct expiration date (RESOLVED)
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) #+ datetime.timedelta(days = 1)
    options['expirationDate'] = options['expirationDate'].dt.date
    options['dte'] = options['expirationDate'].apply(lambda x: np.busday_count(datetime.datetime.today().date(), x,holidays=holidays))
    #options['dte'] =  np.busday_count(datetime.datetime.today().date(), options['expirationDate'],holidays=holidays)
    #options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days
    
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: "C" in x)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    
    # Drop unnecessary and meaningless columns
    options = options.drop(columns = ['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])
    options.columns = ['symbol', 'strike', 'bid', 'ask', 'volume', 'OI',
       'IV', 'ITM', 'exDate', 'dte', 'CPFlag',
       'mid']
    return options
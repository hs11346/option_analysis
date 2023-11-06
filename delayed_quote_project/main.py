from construct_strategy import *
import pandas as pd

def get_config():
    config = pd.read_csv('config.csv')
    return config.Tickers.to_list(), config

#call = CCS_screener(list_, max_strike_width = 4, min_dte = 0, max_dte = 50, fees = 0.1, min_dist = 1, min_bid = 0.4)
if __name__=="__main__":
    list_, config = get_config()
    freeze_support()
    put = PCS_screener(list_, max_strike_width = 3, min_dte = 5, max_dte = 30, fees = 0.1, min_dist = 1.2, min_bid = 0.23)
    freeze_support()
    call = CCS_screener(list_, max_strike_width = 3, min_dte = 5, max_dte = 30, fees = 0.1, min_dist = 1.2, min_bid = 0.23)
    rsi_list = px_screener(config, upper = 70, lower = 30)
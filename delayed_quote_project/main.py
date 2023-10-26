from construct_strategy import *
import pandas as pd

config = pd.read_csv('config.csv')
list_ = config.Tickers.to_list()[:3]

#call = CCS_screener(list_, max_strike_width = 5, min_dte = 0, max_dte = 25, fees = 0.1, min_dist = 0, min_bid = 0)
put = PCS_screener(list_, max_strike_width = 5, min_dte = 0, max_dte = 25, fees = 0.1, min_dist = 0, min_bid = 0)

rsi_list = RSI_screener(config, upper = 70, lower = 30)
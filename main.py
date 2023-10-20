from construct_strategy import *
import pandas as pd

config = pd.read_csv('config.csv')
list_ = config.Tickers.to_list()

df = CCS_screener(['GLD'], max_strike_width = 4, min_dte = 0, max_dte = 30, fees = 0.1, min_dist = 0, min_bid = 0)
import eikon as ek
import pandas as pd
import numpy as np

ek.set_app_key("APP KEY HERE")
df = ek.get_timeseries('AAPL.O',['Bid','Ask','Bidsize','Asksize'], start_date = "2023-09-01T09:30:00", end_date = "2023-09-01T09:35:00", interval="taq")
x = ek.get_timeseries('AAPL.O',['TRADE_ID','TRD_STATUS','TRDPRC_1'], start_date = "2023-09-01T09:30:00", end_date = "2023-09-01T09:35:00", interval="tas")
df = ek.get_timeseries('AAPL.O',['Bid','Ask','Bidsize','Asksize'], start_date = "2023-09-01T09:30:00", end_date = "2023-09-01T09:35:00", interval="taq")

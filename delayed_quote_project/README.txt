This is the directory for the option scrapping project

Two methods are used: yfinance and cboe. yfinance api is compact and easy to use, but there exist data problems and slight inaccuracies, such as the removal of the bid ask prices after market closes, which also impacted IV calculations. CBOE data can be scrapped through the link in JSON format, which is then extracted into Dataframe. This source is preferable given that CBOE data is probably more accurate and contains timestamp from which the data is taken. 

However, the screeners were written for the yfinance dataset, so before cboe data can be done, it must be converted to the yfinance option chain format. There are two screeners that are used by my trading personally, which are the PCS and CCS selling strategies. 

#https://github.com/LSEG-API-Samples/Tutorial.EikonAPI.Python.Streaming/blob/master/01%20-%20Eikon%20Data%20API%20-%20StreamingPrices%20as%20a%20cache.ipynb

import eikon as ek
ek.set_app_key('166a7ffcef9b411ba878d7145ca2f55c78aa4b02')
streaming_prices = ek.StreamingPrices(
    instruments = ['0#GDAXM8*.EX'],
    fields   = ['CF_BID','CF_ASK','OPEN_PRC', 'CF_HIGH','CF_LOW', 'CF_CLOSE', 'PUTCALLIND', 'STRIKE_PRC','IMP_VOLT']
)
streaming_prices.open()
df = streaming_prices.get_snapshot()

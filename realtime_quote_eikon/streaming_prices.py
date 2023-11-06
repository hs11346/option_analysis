#https://github.com/LSEG-API-Samples/Tutorial.EikonAPI.Python.Streaming/blob/master/01%20-%20Eikon%20Data%20API%20-%20StreamingPrices%20as%20a%20cache.ipynb
import datetime
import eikon as ek
ek.set_app_key('166a7ffcef9b411ba878d7145ca2f55c78aa4b02')
fields = ['CF_BID','CF_ASK','CF_LAST','CF_TIME']

def display_updated_fields(streaming_price, instrument_name, fields):
    current_time = datetime.datetime.now().time()
    print(current_time, "- Update received for", instrument_name, ":", fields)
def display_status(streaming_price, instrument_name, status):
    current_time = datetime.datetime.now().time()
    print(current_time, "- Status received for", instrument_name, ":", status)
def display_complete_snapshot(streaming_prices):
    current_time = datetime.datetime.now().time()
    print(current_time, "- StreamingPrice is complete. Full snapshot:")
    print(streaming_prices.get_snapshot())
streaming_prices = ek.StreamingPrices(
    instruments = ['CNY=','JPY=','GBP=','AUD='],
    fields = fields,
    on_refresh=lambda streaming_price, instrument_name, fields: display_updated_fields(streaming_price, instrument_name, fields),
    on_update=lambda streaming_price, instrument_name, fields: display_updated_fields(streaming_price, instrument_name, fields),
    on_status=lambda streaming_price, instrument_name, status: display_status(streaming_price, instrument_name, status),
    #on_complete=lambda streaming_price: display_complete_snapshot(streaming_price)
)
while True:
    streaming_prices.open()


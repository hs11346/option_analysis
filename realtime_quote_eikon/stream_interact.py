#https://github.com/LSEG-API-Samples/Tutorial.EikonAPI.Python.Streaming/blob/master/01%20-%20Eikon%20Data%20API%20-%20StreamingPrices%20as%20a%20cache.ipynb
import datetime
import eikon as ek
from threading import Thread
from queue import Queue
import json
ek.set_app_key('166a7ffcef9b411ba878d7145ca2f55c78aa4b02')
fields = ['CF_BID','CF_ASK','CF_LAST','CF_TIME']

def market_data_stream(out_q):
    def display_updated_fields(streaming_price, instrument_name, fields):
        current_time = datetime.datetime.now().time()
        #print(current_time, "- Update received for", instrument_name, ":", fields)
        print({'Timestamp':str(current_time), "Ticker":instrument_name, "Fields":fields})
        out_q.put({'Timestamp':str(current_time), "Ticker":instrument_name, "Fields":fields})
    def display_status(streaming_price, instrument_name, status):
        current_time = datetime.datetime.now().time()
        print(current_time, "- Status received for", instrument_name, ":", status)
    streaming_prices = ek.StreamingPrices(
        instruments = ['JPY=','AUD=','GBP=','FXY'],
        fields = fields,
        on_refresh=lambda streaming_price, instrument_name, fields: display_updated_fields(streaming_price, instrument_name, fields),
        on_update=lambda streaming_price, instrument_name, fields: display_updated_fields(streaming_price, instrument_name, fields),
        on_status=lambda streaming_price, instrument_name, status: display_status(streaming_price, instrument_name, status),

    )
    while True:
        streaming_prices.open()

def read_market_data(in_q):
    while True:
        fields = in_q.get()
        json.dump(fields, open("log.txt", 'a+'))
        hs = open("log.txt", "a")
        hs.write("\n")
q = Queue()
t1 = Thread(target = market_data_stream, args =(q, ))
t2 = Thread(target = read_market_data, args =(q, ))
t1.start()
t2.start()
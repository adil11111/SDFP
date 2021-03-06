#test file to practice producing graphs :3
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd
import json
from util import crypto

#BUG - 2018/12/16 IS MESSED UP ON NOMICS FOR BTCETH EXCHANGE ON BINANCE - NOT SURE WHY?
#avoid that date lmao

#api key stuff
with open('keys/plotly.json', 'r') as data:
    api_dict = json.load(data)

API_KEY = api_dict['API']
USERNAME = api_dict['username']

#plotly requires you to set the credentials using their module
plotly.tools.set_credentials_file(username = USERNAME, api_key = API_KEY)

'''
Parameters:
data - url to a csv file, or path to csv file (we use url)
market - the name of the graph, usually the market its tracking
'''
def gen_candlestick(data, market):
    '''Method returns HTML code that points to a candlestick graph generated by plotly'''
    try:
        new_header = ['timestamp', 'low', 'open', 'close', 'high', 'volume', 'num_trades']
        df = pd.read_csv(data)
        df.columns = new_header
        '''
        debugging
        print(df)
        print(df.columns)
        print(df.index)
        '''
        trace = go.Ohlc(x=df['timestamp'],
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])
        data = [trace]
        url = py.plot(data, filename=market, auto_open=False)
        #print(url.resource)
        html = tls.get_embed(url)
        return html
    except:
        return "</center>error, check api keys</center>"

'''
Parameters
start - required, the start date to track from
end - optional, if not provided, will use the current date, otherwise this will be the end date
'''
def BTC_price(start, end = None):
    '''Provides a chart of BTC from the dates specified'''
    try:
        if end == None:
            return gen_candlestick(crypto.candlestick_csv_url('1d', 'BTC', start), 'BTC ' + start + ' to today' )
        else:
            return gen_candlestick(crypto.candlestick_csv_url('1d', 'BTC', start, end),  'BTC ' + start + ' to ' + end)
    except:
        return "<center>Error, check api keys</center>"

#Debuggin print statements
#print(gen_candlestick(crypto.candlestick_csv_url('1d', 'BTC', '2018-11-01' , '2018-12-01'), "BTC 2018-11-01 to 2018-12-01"))
#print(gen_candlestick(crypto.candlestick_csv_url('1m', 'ETH', '2018-03-30', '2018-06-01'), 'BTC 2018-04-01 to 2018-06-01'))
#print(gen_candlestick(crypto.candlestick_csv_url('1d', 'BTC', '2018-01-14'), 'BTC All Time'))
#print(BTC_price("2018-01-14"))
#print(BTC_price("2018-01-14", "2018-02-14"))

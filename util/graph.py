#test file to practice producing graphs :3
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd
import crypto

#BUG - 2018/12/16 IS MESSED UP ON NOMICS FOR BTCETH EXCHANGE ON BINANCE - NOT SURE WHY?
#avoid that date lmao

def gen_candlestick(data, market):
    new_header = ['timestamp', 'low', 'open', 'close', 'high', 'volume', 'num_trades']
    df = pd.read_csv(data)
    df.columns = new_header
    print(df)
    print(df.columns)
    print(df.index)

    trace = go.Ohlc(x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])
    data = [trace]
    url = py.iplot(data, filename=market)
    #print(url.resource)
    html = tls.get_embed(url.resource)
    return html

#print(gen_candlestick(crypto.candlestick_csv_url('1d', 'BTC', '2018-11-01' , '2018-12-01'), "BTC 2018-11-01 to 2018-12-01"))
#print(gen_candlestick(crypto.candlestick_csv_url('1m', 'ETH', '2018-03-30', '2018-06-01'), 'BTC 2018-04-01 to 2018-06-01'))


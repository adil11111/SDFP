#test file to practice producing graphs :3
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd
import crypto

#BUG - doesn't print out the candlestick as expected... why?
def gen_candlestick(data, market):
    new_header = ['timestamp', 'low', 'open', 'close', 'high', 'volume', 'num_trades']
    df = pd.read_csv(data)
    df.columns = new_header
    print(df)
    trace = go.Ohlc(x=df['timestamp'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])
    data = [trace]
    url = py.iplot(data, filename=market)
    print(url.resource)
    html = tls.get_embed(url.resource)
    return html

#print(gen_candlestick(crypto.exchange_candles_csv_url('1m', 'binance', 'BTCETH', '2018-12-01' , '2018-12-30'), "BTCETH"))

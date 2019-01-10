#test file to practice producing graphs :3
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

trace = go.Ohlc(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])
data = [trace]
url = py.iplot(data, filename='simple_candlestick')
print(url.resource)
html = tls.get_embed(url.resource)
print(html)

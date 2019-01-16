import json, urllib.request

API_LINK = "https://api.nomics.com/v1/"

with open('keys/nomics.json', 'r') as data:
    api_dict = json.load(data)

API_KEY = api_dict['API']

def coins():
    '''Returns a dictionary of all the currencies available on Nomics'''
    url = API_LINK + 'currencies?key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def prices():
    '''Returns the prices for all the currencies on Nomics'''
    url = API_LINK + 'prices?key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def prices_sparkline(start, end):
    '''Returns list of sparkline data related to all the currencies on Nomics'''
    url = API_LINK + 'currencies/sparkline?key=' + API_KEY + "&start=" + start + "T00%3A00%3A00Z&end=" + end + "T00%3A00%3A00Z"
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def candlestick(interval, currency, start = None, end = None):
    '''Returns candlestick data regarding a certain currency, priced in USD, in JSON format '''
    if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&end=" + end + "T00%3A00%3A00Z"
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z"
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z&end=" + end + "T00%3A00%3A00Z"
        response = urllib.request.urlopen(url)
        return json.loads(response.read())

def candlestick_csv(interval, currency, start = None, end = None):
    '''Returns candlestick data regarding a certain currency, priced in USD, in CSV format '''
    if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response 
    elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&end=" + end + "T00%3A00%3A00Z" + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response 
    elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z" + "&format=csv" 
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response 
    else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z&end=" + end + "T00%3A00%3A00Z" + "&format=csv" 
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response 

def candlestick_csv_url(interval, currency, start = None, end = None):
    '''Returns a url pointing to a csv file that has candlestick data regarding a certain currency, priced in USD'''
    if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&format=csv"
        return url
    elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&end=" + end + "T00%3A00%3A00Z" + "&format=csv"
        return url
    elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z" + "&format=csv" 
        return url
    else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&currency=' + currency + "&start=" + start + "T00%3A00%3A00Z&end=" + end + "T00%3A00%3A00Z" + "&format=csv" 
        print(url)
        return url

def exchange_candles(interval, exchange, market, start = None, end = None):
    '''Returns candlestick data related to exchange rates in JSON format'''
    if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&end=' + end + 'T00%3A00%3A00Z'
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' 
        response = urllib.request.urlopen(url)
        return json.loads(response.read())
    else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' + '&end=' + end + 'T00%3A00%3A00Z'
        response = urllib.request.urlopen(url)
        return json.loads(response.read())

def exchange_candles_csv(interval, exchange, market, start = None, end = None):
      '''Returns candlestick data related to exchange rates in CSV format'''
      if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response
      elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&end=' + end + 'T00%3A00%3A00Z' + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response
      elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response
      else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' + '&end=' + end + 'T00%3A00%3A00Z' + "&format=csv"
        response = urllib.request.urlopen(url).read().decode("utf8")
        return response

def exchange_candles_csv_url(interval, exchange, market, start = None, end = None):
    '''Returns a url pointing to a CSV file with candlestick atat related to exchange rates'''
    if start == None and end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + "&format=csv"
        return url 
    elif start == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&end=' + end + 'T00%3A00%3A00Z' + "&format=csv"
        return url 
    elif end == None:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' + "&format=csv"
        return url
    else:
        url = API_LINK + 'candles?key=' + API_KEY + '&interval=' + interval + '&exchange=' + exchange + '&market=' + market + '&start=' + start + 'T00%3A00%3A00Z' + '&end=' + end + 'T00%3A00%3A00Z' + "&format=csv"
        return url

def markets():
    '''Returns data regarding the markets Nomics supports '''
    url = API_LINK + "markets?key=" + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def list_exchanges():
    '''Returns a list of all the exchanges supproted on Nomics'''
    list_of_exchanges = []
    raw = markets()

    for dict in raw:
        if not dict['exchange'] in list_of_exchanges:
            list_of_exchanges.append(dict['exchange'])

    return list_of_exchanges

def list_markets_available(exchange):
    '''Returns a list of markets available, when given a certain exchange'''
    list_of_markets = []
    raw = markets()

    for dict in raw:
        if dict['exchange'] == exchange:
            list_of_markets.append(dict['market'])

    return list_of_markets

def dashboard():
    '''Returns dashboard information regarding all the currencies on Nomics in JSON format'''
    url = API_LINK + "dashboard?key=" + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def list_coins():
    '''Returns a list of coins available on the Nomics API'''
    list_of_coins = []
    raw = coins()
    for dict in raw:
        list_of_coins.append(dict['id'])
    return list_of_coins

    

#testing functions
#All work as intended, unless otherwise stated
#print(prices())
#print(list_coins())
#print(prices_sparkline("2018-12-01", "2018-12-31"))
#print(candlestick('1d', 'BTC'))
#print(exchange_candles('1m', 'binance', 'BTCETH', "2018-12-01"))
#print(exchange_candles('1m', 'binance', 'BTCETH', None, '2018-12-30'))
#print(exchange_candles('1m', 'binance', 'BTCETH', '2018-12-01' , '2018-12-30'))
#print(exchange_candles_csv('1m', 'binance', 'BTCETH', '2018-12-01' , '2018-12-30'))
#print(dashboard())
#print(markets())
#print(list_exchanges())
#print(list_markets_available("binance"))

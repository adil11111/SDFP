import json, urllib.request

API_LINK = "https://api.nomics.com/v1/"

with open('../data/keys.json', 'r') as data:
    api_dict = json.load(data)

API_KEY = api_dict['nomics']

#everything works as intended, unless otherwise commented!

def coins():
    url = API_LINK + 'currencies?key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def prices():
    url = API_LINK + 'prices?key=' + API_KEY
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def prices_sparkline(start, end):
    url = API_LINK + 'currencies/sparkline?key=' + API_KEY + "&start=" + start + "T00%3A00%3A00Z&end=" + end + "T00%3A00%3A00Z"
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def list_coins():
    list_of_coins = []
    raw = coins()
    for dict in raw:
        list_of_coins.append(dict['id'])
    return list_of_coins

#testing functions
#print(prices())
print(list_coins())
#print(prices_sparkline("2018-12-01", "2018-12-31"))

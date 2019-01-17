from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions
import sqlite3

import os, random

from util import dbEditor, crypto

try:
    from util import graph
except:
    print('graph error')
app = Flask(__name__)

app.secret_key = os.urandom(32)

#Dictionary of topics
goodTopics={'btc_economy':"Bitcoin Economy",
            'btc_tech':"Bitcoin Technology",
            'btc_news':"Bitcoin News",
            'eth_economy':"Ethereum Economy",
            'eth_tech':"Ethereum Technology",
            'eth_news':"Ethereum News",
            'alt_economy':"Alt Coins Economy",
            'alt_tech':"Alt Coins Technology",
            'alt_news':"Alt Coins News",
            'gen_meta':"General: Meta",
            'gen_tech':"General: Technology",
            'gen_tips':"General: Investment Tips"}


#returns whether a user is logge in or not :3
def noUser():
    return 'username' not in session.keys()

def notificationJoiner(l):
    # pass this the call of getUnreadNotifs and it'll create the message to "alert"
    # then link it to the l[2] and l[3].
    user = l[0]
    action = l[1]
    strToReturn = "@" + user + action + "your post."

@app.route("/")
def root():
    return render_template('home.html', notLoggedIn=noUser())

"""login logout"""
@app.route("/auth", methods=["POST"])
def authentication():
    user = request.form['username']
    password = request.form['password']

    db = sqlite3.connect('data/base.db')
    c = db.cursor()
    #dbEditor.reset(c)

    if dbEditor.check_pass(c,user,password):
        session['username'] = user
        db.close()
        return redirect('/profile')

    else:
        flash("Incorrect Login Information")
        return redirect('/')


@app.route('/logout')
def logout():
    #pop user from session
    if noUser():
        redirect('/')
    session.pop('username')
    return redirect('/')


"""register"""
@app.route("/register_page")
def register_page():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register_auth():
    user=request.form['username']
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if not dbEditor.userExists(c,user):
        password1 = request.form['password1']

        password2 = request.form['password2']

        if (password1 == password2):
            dbEditor.addUser(c,user,password1)
            db.commit()
            flash('Registration Successful!')
            db.close()
            return redirect('/')
        else:
            db.close()
            flash('Passwords do not match.')
            return redirect('/register_page')
    db.close()
    flash('Username already taken')
    return redirect('/register_page')


"""profile"""
@app.route('/profile', methods=['POST', 'GET'])
def load_profile():
    if noUser():
        return redirect('/')
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if request.method=='GET':
        coins = dbEditor.getCoins(c,session['username'])
        threads = dbEditor.userThreads(c, session['username'])
        posts = dbEditor.userPosts(c,session['username'])
        #threads=[[post, id],[etc]]

        readPosts = dbEditor.getReadNotifs(c,session['username'])
        readPosts = dbEditor.getReadNotifs(c,session['username'])

        #[[user,post,thread_id, postid]]
        unreadPosts = dbEditor.getUnreadNotifs(c,session['username'])
        #[[user,post,threadid, postid]]
        db.close()
        return render_template('profile.html', coins=coins, threads=threads, posts=posts,read_posts=readPosts, unread_posts=unreadPosts,user=session['username'])
    else:
        pid = request.form['pid']
        tid = request.form['tid']

        if request.form['act'] == 'read':#read value
            dbEditor.readNotif(c,session['username'],tid,pid)
            db.commit()
            db.close()
            return redirect('/thread?id='+tid+"#"+pid)
        else:
            db.close()
            return redirect('/thread?id='+tid+"#"+pid)

"""forum """
@app.route("/forum", methods=['POST', 'GET'])
def load_forum():
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    topic = request.args.get('topics')

    if topic not in goodTopics.keys():
        flash('Oops, this topic is not yet available')
        return redirect('/')

    threads = dbEditor.viewTopic(c, topic)

    #print(threads)
    #could edit topic to make more English, or display as is, as now is
    #threads=[[id, post,user],[etc]] from specific topic

    db.close()
    englishtopic = goodTopics[topic]

    return render_template('forum.html', notLoggedIn=noUser(),topic=englishtopic, idtopic=topic, threads= threads)

@app.route("/mkthr", methods = ['POST'])
def makeThread():
    post = request.form["initPost"]
    topic = request.form["topic"]#will return as rendered in load_forum

    if noUser():#allow for not logged-in posting
        flash('Not logged in')
    else:
        user = session['username']
        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        dbEditor.newThread(c,post,user,topic)
        db.commit()
        db.close()

    return redirect('/forum?topics='+topic)


"""thread"""
@app.route("/thread", methods=['POST','GET'])
def load_thread():
    if request.method == "GET":
        threadID = request.args.get('id')#or perhaps name?
        print(threadID)
        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        try:
            posts = dbEditor.viewThread(c, threadID)
            #posts=[[user, post, timestamp, upvotes],[etc]] as of now, of specific thread
            #dummyPostforTesting=[["Math", "how can you calculate bitcoins","tomorrow",-100]]
            db.close()
            return render_template('thread.html', notLoggedIn=noUser(), posts=posts, threadname=posts[0][1], threadID=threadID)
        except:
            flash("Thread not Found")
            return redirect('/')

    else:
        """Upvote???"""
        #if wants to incorporate this, would need some login requirement, and disable function dependent on user record...
        info = request.form['upvote'].split(',')
        postID = info[0]
        threadID = info[1]

        if not noUser():
            db = sqlite3.connect('./data/base.db')
            c = db.cursor()
            dbEditor.votePost(c,threadID, postID,1,session['username'])
            db.commit()

        #function to add upvote
        return redirect('/thread?id='+threadID)


@app.route("/addPost", methods=['POST'])
def addPost():
    """addPosts"""
    threadid = request.form['id']
    content = request.form['post']

    """prevents anonymos posting"""
    if noUser():
        flash("No user")

    else:
        user = session['username']

        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        dbEditor.addToThread(c, content, threadid, user)

        db.commit()
        db.close()

    return redirect('/thread?id='+threadid)

'''Displays any releveant chart data if the user submitted something. Otherwise just tracks the price of BTC, going back a year'''
@app.route("/chart", methods=['POST', 'GET'])
def chart():
    stuff = "<center><h3>BitCoin Price</h3></center>" + graph.BTC_price("2018-01-15")
    graph_title = ''

    try:
        stuff += '<center><h5> Either you didn\'t submit something, or the API can\'t find valid data in that date range. Try again!</center></h5>'
        #checks the method type
        #POST means its a price graph
        #GET means it's a exchange/market graph

        if request.method == 'POST':
            start = request.form.get('start')
            end = request.form.get('end')
        else:
            start = request.args.get('start')
            end = request.args.get('end')

        market = request.args.get('market')
        exchange = request.args.get('exchange')

        if market == None or exchange == None:
            csv_url =  crypto.candlestick_csv_url('1d', request.form.ge('coin'), start, end)
            graph_title = request.form.get('coin') + ' Price'
            stuff = graph.gen_candlestick(csv_url, request.form.get('coin') + graph_title)
        else:
            csv_url = crypto.exchange_candles_csv_url('1d', exchange, market, start, end)
            graph_title = request.args.get('market') + ' price on ' + request.args.get('exchange')
            stuff = graph.gen_candlestick(csv_url, graph_title)
        #print(stuff)
        return render_template('charts.html', notLoggedIn=noUser(), stuff = '<center><h3>' + graph_title + '</center></h3>' + stuff)
    except:
        return render_template('charts.html', notLoggedIn=noUser(), stuff = '<center><h3>' + graph_title + '</center></h3>' + stuff)

@app.route("/coins")
def coins():
    '''uses the Nomics API dashboard data to bring a dashboard that is updated every 15 seconds'''
    try:
        big_dict=crypto.dashboard()
    except:
        big_dict=[]
    return render_template('coins.html', big_dict = crypto.dashboard(), notLoggedIn = noUser())

@app.route("/prices")
def prices():
    '''get's the list of coins for the user to check the price of, and allows them to choose'''
    try:
        coins = crypto.list_coins()
    except:
        flash("unable to get list of coins")
        #print('cant get coins!')
        coins=[]

    return render_template('prices.html', notLoggedIn=noUser(), coins=coins)

'''Allows the user to pick an exchange, a market on that exchange, and view stats for it'''
@app.route("/exchanges", methods=['POST', 'GET'])
def exchanges():
    exchange = request.args.get('exchange')

    if exchange == None:
        return render_template('exchange.html', exch_picked=False, exchanges = crypto.list_exchanges())
    else:
        return render_template('exchange.html', exch_picked=True, markets = crypto.list_markets_available(exchange), exchange_chosen = exchange)

if __name__=="__main__":
    app.debug = True
    app.run()

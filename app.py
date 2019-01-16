from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions
import sqlite3

import os, random

from util import dbEditor, crypto#, graph
try:
    from util import graph
except:
    print('graph error')
app = Flask(__name__)

app.secret_key = os.urandom(32)

goodTopics=['btc_economy', 'btc_tech','btc_news',
            'eth_economy', 'eth_tech','eth_news',
            'alt_economy', 'alt_tech','alt_news',
            'gen_meta', 'gen_tech','gen_investment']

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
    user=request.form['username']
    password=request.form['password']
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    #dbEditor.reset(c)

    if dbEditor.check_pass(c,user,password):
        session['username']=user
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
        password1=request.form['password1']
        password2=request.form['password2']

        if (password1==password2):
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
@app.route('/profile')
def load_profile():
    if noUser():
        return redirect('/')
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if request.method=='GET':

        coins=dbEditor.getCoins(c,session['username'])
        threads=dbEditor.userThreads(c, session['username'])
        posts=dbEditor.userPosts(c,session['username'])
        #threads=[[post, id],[etc]]
        readPosts=dbEditor.getReadNotifs(c,session['username'])
        #[[user,post,thread_id, postid]]
        unreadPosts=dbEditor.getUnreadNotifs(c,session['username'])
        #[[user,post,threaid, postid]]
        db.close()
        return render_template('profile.html', coins=coins, threads=threads, posts=posts,read_posts=readPosts, unread_posts=unreadPosts)
    else:
        pid=request.form['pid']
        tid=request.form['tid']
        if request.form['act']=='read':#read value
            dbEditor.readNotif(c,session['username'],tid,pid)
            db.commit()
            db.close()
            return redirect('/thread?id=tid#pid')
        else:
            db.close()
            return redirect('/thread?id=tid#pid')






"""forum """
@app.route("/forum", methods=['POST', 'GET'])
def load_forum():
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    topic = request.args.get('topics')
    if topic not in goodTopics:
        flash('Oops, this topic is not yet avaialbe')
        return redirect('/')
    threads= dbEditor.viewTopic(c, topic)
    print (threads)
    #could edit topic to make more English, or display as is, as now is
    #threads=[[id, post,user],[etc]] from specific topic
    db.close()
    return render_template('forum.html', notLoggedIn=noUser(),topic=topic, threads= threads)

@app.route("/mkthr", methods=['POST'])
def makeThread():
    post=request.form["initPost"]
    topic=request.form["topic"]#will return as rendered in load_forum


    if noUser():#allow for not logged-in posting
        flash('Not logged in')
    else:
        user=session['username']
        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        dbEditor.newThread(c,post,user,"now",topic)
        db.commit()
        db.close()


    return redirect('/forum?topics='+topic)


"""thread"""
@app.route("/thread", methods=['POST','GET'])
def load_thread():

    if request.method=="GET":
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
        info=request.form['upvote'].split(',')
        postID=info[0]
        threadID=info[1]

        if not noUser():
            db = sqlite3.connect('./data/base.db')
            c = db.cursor()
            dbEditor.votePost(c,threadID, postID,1,session['username'])
            db.commit()
            db.close()
        #function to add upvote
        return redirect('/thread?id='+threadID)


@app.route("/addPost", methods=['POST'])
def addPost():
    """addPosts"""
    threadid=request.form['id']
    content=request.form['post']

    """allow for not logged in users to post"""
    if noUser():
        flash("No user")

    else:
        user = session['username']
        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        dbEditor.addToThread(c, content, threadid, user, "datetime")
        db.commit()
        db.close()

    return redirect('/thread?id='+threadid)



@app.route("/chart", methods=['POST', 'GET'])
def chart():
    stuff=""
    try:
        if request.method == 'GET':
            #stuff = graph.BTC_price("2018-01-14")
            stuff=""

        else:
            start = request.form['start']
            end=request.form['end']
            if end==None:
                stuff=graph.BTC_price(start)
            elif start>end:
                stuff=graph.BTC_price(start)
            else:
                stuff = graph.BTC_price(start, end)
                #stuff=""
    except:
        stuff=""
    return render_template('charts.html', notLoggedIn=noUser(), stuff=stuff)

@app.route("/coins")
def coins():
    try:
        big_dict=crypto.dashboard()
    except:
        big_dict=[]
    return render_template('coins.html', big_dict = crypto.dashboard())

@app.route("/prices")
def prices():
    t=request.args.get('type')
    market=[]
    try:
        if t==None:
            coins=crypto.list_coins()
        elif t =="ex":
            coins=[]#exchanges
            market=[]#market
        else:#candlestick
            coins=[]
    except:
        coins=[]
        market=[]
    return render_template('prices.html', notLoggedIn=noUser(), coins=coins, market=market)

"""
read/readnotifs
read:user said this, link back to thread; change to read
user/post/post_id/thread_id/read
"""
if __name__=="__main__":
    app.debug=True
    app.run()

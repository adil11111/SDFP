

from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions
import sqlite3

import os, random

from util import dbEditor

app = Flask(__name__)

app.secret_key = os.urandom(32)


def noUser():
    return 'username' not in session.keys()

@app.route("/")
def root():

    return render_template('home.html', notLoggedIn=noUser())

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
        return render_template('profile.html')

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

@app.route("/chart")
def chart():
    return render_template('charts.html', notLoggedIn=noUser())

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
    


@app.route('/profile')
def load_profile():
    if noUser():
        return redirect('/')
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    coins=dbEditor.getCoins(c,session['username'])
    # want threads=[[post, id],[etc]]
    return render_template('profile.html', coins=coins)

"""forum """
@app.route("/forum")
def load_forum():
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    topic = request.args.get('topics')
    threads= dbEditor.viewTopic(c, topic)
    print (threads)
    #could edit topic to make more English, or display as is
    #threads=[[id, post,user],[etc]] from specific topic
    db.close()
    return render_template('forum.html', notLoggedIn=noUser(),topic=topic, threads= threads)

@app.route("/mkthr", methods=['POST'])
def makeThread():
    post=request.form["initPost"]
    topic=request.form["topic"]#will return as rendered in load_forum

    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if noUser():
        user='Anonymous'
    else:
        user=session['username']
    dbEditor.newThread(c,post,user,"now",topic)
    db.commit()
    db.close()
    print('was here')
    #some function to create thread;
    return redirect('/forum?topics='+topic)


"""thread"""
@app.route("/thread", methods=['POST','GET'])
def load_thread():
    if request.method=="GET":
        threadID = request.args.get('id')#or perhaps name?
        print(threadID)
        db = sqlite3.connect('./data/base.db')
        c = db.cursor()
        posts = dbEditor.viewThread(c, threadID)
        #posts=[[user, post, timestamp, upvotes],[etc]] as of now, of specific thread
        #want threadname
        #want id used somewhere, not sure
        #dummyPostforTesting=[["Math", "how can you calculate bitcoins","tomorrow",-100]]
        db.close()
        return render_template('thread.html', notLoggedIn=noUser(), posts=posts, threadname=posts[0][1], threadID=threadID)
    else:

        #if wants to incorporate this, would need some login requirement, and disable function dependent on user record...
        info=request.form['upvote'].split(',')
        postID=info[0]
        threadID=info[1]
        #function to add upvote
        return redirect('/thread?id='+threadID)
        

@app.route("/addPost", methods=['POST'])
def addPost():
    threadid=request.form['id']
    content=request.form['post']
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if noUser():
        user = "Anonymous"
    else:
        user = session['username']
    dbEditor.addToThread(c, content, threadid, user, "datetime")
    db.commit()
    db.close()
    
    return redirect('/thread?id='+threadid)





if __name__=="__main__":
    app.debug=True
    app.run()

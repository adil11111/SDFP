

from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions
import sqlite3

import os, random

from util import dbEditor

app = Flask(__name__)

app.secret_key = os.urandom(32)









@app.route("/")
def root():
    if 'username' not in session.keys():
        session['noUser']=True
    else:
        session['noUser']=False
    return render_template('home.html', notLoggedIn=session["noUser"])

@app.route("/auth", methods=["POST"])
def authentication():
    user=request.form['username']
    password=request.form['password']
    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    #dbEditor.reset(c)
    if dbEditor.check_pass(c,user,password):
        session["noUser"]=False
        session['username']=user
        db.close()
        return render_template('profile.html')

    else:
        flash("Incorrect Login Information")
        return redirect('/')
    

@app.route('/logout')
def logout():
    #pop user from session
    session.pop('username')
    session["noUser"] = True
    return redirect('/')

@app.route("/chart")
def chart():
    return render_template('charts.html', notLoggedIn=session["noUser"])

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
    return render_template('profile.html')

"""forum """
@app.route("/forum")
def load_forum():
    topic = request.args.get('topics')
    #could edit topic to make more English, or display as is
    #want threads=[[post, id, user],[etc]], as of now, from specific topic
    return render_template('forum.html', notLoggedIn=session["noUser"],topic=topic)

@app.route("/mkthr", methods=['POST'])
def makeThread():
    post=request.form["initPost"]
    topic=request.form["topic"]#will return as rendered in load_forum

    db = sqlite3.connect('./data/base.db')
    c = db.cursor()
    if session["noUser"]:
        user='Anonymous'
    else:
        user=session['username']
    dbEditor.newThread(c,post,user,"now",topic)
    db.commit()
    db.close()
    print('was here')
    #some function to create thread;
    return render_template('forum.html', notLoggedIn=session["noUser"],topic=topic)


"""thread"""
@app.route("/thread", methods=['POST','GET'])
def load_thread():
    if request.method=="GET":
        threadID = request.args.get('id')#or perhaps name?
        #want posts=[[user, post, timestamp, upvotes],[etc]] as of now, of specific thread
        #want threadname
        #want id used somewhere, not sure
        dummyPostforTesting=[["Math", "how can you calculate bitcoins","tomorrow",-100]]
        return render_template('thread.html', notLoggedIn=session["noUser"], posts=dummyPostforTesting)
    else:
        postID=request.form['id']
        #function to add upvote
        return render_template('thread.html', notLoggedIn=session["noUser"])
        

@app.route("/addPost", methods=['POST'])
def addPost():
    #threadid=request.form['id']
    content=request.form['post']
    #some stuff to create content
    return redirect('/thread')





if __name__=="__main__":
    app.debug=True
    app.run()

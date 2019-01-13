

from flask import Flask, render_template
from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions
import sqlite3

from passlib.hash import sha256_crypt
import os, random

from util import dbEditor

app = Flask(__name__)

app.secret_key = os.urandom(32)

noUser=True #general login status

db = sqlite3.connect('data/base.db')
c = db.cursor()


@app.route("/")
def root():
    return render_template('home.html', notLoggedIn=noUser)

@app.route("/auth", methods=["POST"])
def authentication():
    user=request.form['username']
    password=request.form['password']
    if dbEditor.check_pass(c,user,password):
        noUser=False
        session['username']=user
        return render_template('profile.html')

    else:
        flash("Incorrect Login Information")
        return redirect('/')
    

@app.route('/logout')
def logout():
    #pop user from session
    noUser = True
    return redirect('/')

@app.route("/chart")
def chart():
    return render_template('charts.html', notLoggedIn=noUser)

@app.route("/register_page")
def register_page():
    
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register_auth():
    user=request.form['username']
    if not dbEditor.userExists(c,user):
        password1=request.form['password1']
        password2=request.form['password2']
        
        if (password1==password2):
            password1 = sha256_crypt.hash(password1)
            dbEditor.addUser(c,user,password1)
            flash('Registration Successful!')
            return redirect('/')
        else:
            flash('Passwords do not match.')
            return redirect('/register_page')
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
    return render_template('forum.html', notLoggedIn=noUser,topic=topic)

@app.route("/mkthr", methods=['POST'])
def makeThread():
    post=request.form["initPost"]
    topic=request.form["topic"]#will return as rendered in load_forum
    #some function to create thread;
    return render_template('forum.html', notLoggedIn=noUser,topic=topic)


"""thread"""
@app.route("/thread", methods=['POST','GET'])
def load_thread():
    if request.method=="GET":
        threadID = request.args.get('id')#or perhaps name?
        #want posts=[[user, post, timestamp, upvotes],[etc]] as of now, of specific thread
        #want threadname
        #want id used somewhere, not sure
        dummyPostforTesting=[["Math", "how can you calculate bitcoins","tomorrow",-100]]
        return render_template('thread.html', notLoggedIn=noUser, posts=dummyPostforTesting)
    else:
        postID=request.form['id']
        #function to add upvote
        return render_template('thread.html', notLoggedIn=noUser)
        

@app.route("/addPost", methods=['POST'])
def addPost():
    #threadid=request.form['id']
    content=request.form['post']
    #some stuff to create content
    return redirect('/thread')





if __name__=="__main__":
    app.debug=True
    app.run()

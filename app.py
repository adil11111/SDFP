from flask import Flask, render_template

from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

import os, random

app = Flask(__name__)

app.secret_key = os.urandom(32)

noUser=True #general login status

@app.route("/")
def root():
    
    return render_template('home.html', notLoggedIn=noUser)

@app.route("/auth", methods=["POST"])
def authentication():

    
    return "quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appelantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit."

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

@app.route("/register")
def register_auth():
    return redirect('/')


@app.route('/profile')
def load_profile():
    return render_template('profile.html')

"""thread and forum """
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

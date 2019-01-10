from flask import Flask, render_template

from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

import os, random

app = Flask(__name__)

app.secret_key = os.urandom(32)


@app.route("/")
def root():
    
    return render_template('home.html', notLoggedIn=True)

@app.route("/auth", methods=["POST"])
def authentication():

    
    return "quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appelantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit."

@app.route("/chart")
def chart():
    return render_template('charts.html')

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
    return render_template('forum.html')

@app.route("/thread")
def load_thread():
    threadID = request.args.get('id')#or perhaps name?
    return render_template('thread.html')





if __name__=="__main__":
    app.debug=True
    app.run()

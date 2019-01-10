from flask import Flask, render_template

from flask import request, session #login function
from flask import url_for, redirect, flash #redirect functions

import os, random

app = Flask(__name__)

app.secret_key = os.urandom(32)


@app.route("/")
def root():
    
    return render_template('home.html')

@app.route("/auth", methods=["POST"])
def authentication():

    
    return "quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appelantur. Hi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit."


if __name__=="__main__":
    app.debug=True
    app.run()

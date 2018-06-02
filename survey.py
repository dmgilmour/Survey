import json
from flask import Flask, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = 


@app.route("/")
def default():

    return render_template("login.html")

@app.route("/register")
def register():
    message = ""

    if request.method == "POST":
        # if not already found
        if not User.query.filter_by(name=request.form["user"]).all():
            #db.session.add(User(request.form["user"], request.form["pass"]))
            #db.session.commit()
            #message = "



"""
    
        




app.secret_key = "git git git brrrrrwrwrwaaahh"

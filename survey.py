import json
import re
import random
from flask import Flask, request, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from postmastergeneral import PostMasterGeneral

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

regex = '[a-zA-Z]{3,6}[0-9]{1,3}'

ronaldStroman = PostMasterGeneral()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    registerred = db.Column(db.Boolean, default = False) 
    reg_code = db.Column(db.String(16))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def generate_reg_code(self):
        r = random.randint(0, 16777216)
        self.reg_code = hex(r)[2:] # make hex and remove the '0x' at the beginning
        self.reg_code += str(self.id)
        ronaldStroman.sendRegistrationEmail(self.name + '@pitt.edu', self.reg_code)



@app.cli.command("initdb")
def initdb():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route("/")
def default():
    
    return render_template("login.html")

@app.route("/login")
def login():

    # if loggedin
        # return redirect(url_for("home"))
    # else
    return render_template("home.html")



@app.route("/register/", methods = ["GET", 'POST'])
def register():
    message = ""

    if logged_in():
        return redirect(url_for("home"))

    if request.method == "POST":
        # if not already found
        name = request.form["user"]
        if not User.query.filter_by(name=name).all():

            reg_compile = re.compile(name)
            print(name)
            if reg_compile.search(regex, 0) == None:
                message = "Incorrect email format"
            else:

                db.session.add(User(request.form["user"], request.form["pass"]))
                User.query.filter_by(name=name).first().generate_reg_code()
                db.session.commit()
                message = "Regristration link sent"

        else:
            message = "Name in use"

    return render_template("register.html", message=message)


@app.route("/register/<code>/")
def confirm(code):
    user_id = int(code[6:]) # grab userid from 7th char on
    user = User.query.filter_by(id=user_id).first()
    if user != None:
        if code[:7] == user.reg_code: # get the registration code without user id and verify
            return render_template("success.html")
            
        else:
            return render_template("failure.html")
    else:
        return render_template("failure.html")

        
def logged_in():
    if "user" in session:
        #if not User.query.filter_by(name=session["user"]).first():
        #    session.clear()
        #    return False
        #else:
        #    return True
        return True
    else:
        return False

        




app.secret_key = "git git git brrrrrwrwrwaaahh"

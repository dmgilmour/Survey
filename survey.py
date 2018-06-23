import json
import re
import random
from flask import Flask, request, url_for, redirect, session, render_template, flash
from datetime import datetime
from postmastergeneral import PostMasterGeneral
from user import User
from shared_model import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

regex = '[a-zA-Z]{3,6}[0-9]{1,3}'

meganBrennan = PostMasterGeneral()



@app.cli.command("initdb")
def initdb():
    db.drop_all()
    db.create_all()
    db.session.commit()



@app.route("/")
def home():
    login_wall()
    return render_template("home.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        user = User.query.filter_by(name = request.form["user"]).first()
        if user:
            if request.form["pass"] == user.password:
                if user.registered:
                    session["user"] = request.form["user"]
                    return redirect(url_for("home"))
                else:
                    message = "Registration incomplete"
            else:
                message = "Invalid credentials"
        else:
            message = "Invalid credentials"
    return render_template("login.html", message = message)
    


@app.route("/register/", methods = ["GET", 'POST'])
def register():
    message = ""

    if logged_in():
        return redirect(url_for("home"))

    if request.method == "POST":
        # if not already found
        name = request.form["user"]
        if not User.query.filter_by(name=name).all():

            #reg_compile = re.compile(name)
            #print(name)
            #if reg_compile.search(regex, 0) == None:
            #    message = "Incorrect email format"
            #else:

            db.session.add(User(request.form["user"], request.form["pass"]))
            new_user = User.query.filter_by(name=name).first()

            reg_code = generate_reg_code(new_user) 
            new_user.reg_code = reg_code
            meganBrennan.sendRegistrationEmail(new_user.name, reg_code)

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
            user.registered = True
            db.session.commit()
            return redirect(url_for("home"))
        else:
            return render_template("failure.html")
    else:
        return render_template("failure.html")


@app.route("/logout/")
def logout():
    if "user" in session:
        session.clear()
    return redirect(url_for("login"))

        
def logged_in():
    if "user" in session:
        if not User.query.filter_by(name=session["user"]).first():
            session.clear()
            return False
        else:
            return True
    else:
        return False

        
def login_wall():
    if logged_in():
        pass
    else:
        return redirect(url_for("login"))


def generate_reg_code(user):

    # Random 6 char hex code with user id # appended on the end
    reg_code = hex(random.randint(0, 16777216))[2:]  # [2:] to get rid of the '0x' 
    return reg_code + str(user.id)




app.secret_key = "git git git brrrrrwrwrwaaahh"

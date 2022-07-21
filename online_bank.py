"""
Authors: Alex, John
Class:
Date: 2022-07-18

Execute:
  export FLASK_APP=online_bank.py
  flask run
  Web Browser navigate to http://127.0.0.1:5000/
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from login import create, verify, change

#Tracks the logged-in user
LOGGED_IN = None

#Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    """
    Main landing page
    """
    return render_template("index.html", cur_date=datetime.now())

@app.route("/hello/")
def hello(name=None):
    """
    Page prints hello <name>
    """
    return render_template("hello.html", name=name)
    
@app.route("/home/")
def home(current_user=None):
    """
    Home page after logging in
    """
    if LOGGED_IN:
        return render_template("home.html", name=LOGGED_IN)
    return redirect(url_for("login"))

@app.route("/register/", methods=["GET", "POST"])
def register():
    """
    Render method for register page
    """
    if request.method == "POST":
        error = create(request.form["username"], request.form["password"])

        if error is None:
            flash("User successfully registered.")
            return redirect("/login/")
        flash(error)

    return render_template("register.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Render method for login page
    """
    if request.method == "POST":
        if verify(request.form["username"], request.form["password"]):
            global LOGGED_IN
            LOGGED_IN = request.form["username"]
            flash("Successfully logged in.")
            return redirect("/home/")

        flash("Invalid username or password.")

    return render_template("login.html")
    
@app.route("/update/", methods=["GET", "POST"])
def update():
    """
    Render method for update page
    """
    if request.method == "POST":
        error = change(LOGGED_IN, request.form["password"])

        if error is None:
            flash("Successfully updated password.")
            return redirect("/home/")

        flash(error)

    return render_template("update.html", LOGGED_IN=LOGGED_IN)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    """
    Render method for logging out
    """
    
    global LOGGED_IN
    LOGGED_IN = None
    flash("Successfully logged out.")
    return redirect("/")
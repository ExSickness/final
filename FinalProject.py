'''
Authors:
Class:
Date:

Execute:
  export FLASK_APP=FinalProject.py
  flask run
  Web Browser navigate to http://127.0.0.1:5000/
'''

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# from passlib.hash import sha256_crypt
from hashlib import sha256
from string import punctuation, ascii_lowercase, ascii_uppercase, digits

app = Flask("lab8")
app.secret_key = "secret"
app.secret = "secret"

authenticated_users = []
log = []

@app.route("/")
def index():
    '''
    Main landing page
    '''
    return render_template('index.html', cur_date=datetime.now())

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    '''
    Page prints hello <name>
    '''
    return render_template("hello.html", name=name)

def user_exists(user):
    with open("creds.txt", "r+") as f:
        for line in f.readlines():
            cur_user, cur_pass = line.split(" ")
            # print("cur_user:", cur_user)
            # print("user:", user)
            # print("username == cur_user:", username == cur_user)
            if user == cur_user:
                return True

    return False

def validate_creds(username, password):
    with open("creds.txt", "r+") as f:
        # print("opened file")
        for line in f.readlines():
            # print("curline:", line)
            cur_user, cur_pass = line.split(" ")
            # print("username:", username)
            # print("cur_user:", cur_user)
            # print("password:", password)
            # print("cur_pass:[", cur_pass.strip(), "]")
            # print()
            # print("username == cur_user:", username == cur_user)
            # print("password == cur_pass.strip():", password == cur_pass.strip())
            # print("username == cur_user and password == cur_pass:", username == cur_user and password == cur_pass.strip())
            if username == cur_user and password == cur_pass.strip():
                print("creds found")
                return True

    print("creds not found")
    return False

def validate_pass(password):
    if len(password) < 12 or \
            not any(cur in ascii_lowercase for cur in password) or \
            not any(cur in ascii_uppercase for cur in password) or \
                not any(cur in punctuation for cur in password) or \
                     not any(cur in digits for cur in password):
        print("criteria fail")
        return False

    with open("CommonPassword.txt", "r+") as f:
        for line in f.readlines():
            if line == password:
                print(f"line == password {line} == {password}")
                return False

    return True

@app.route('/register/', methods=['GET','POST'])
def register():
    '''
    Page prompts user to enter username/password into a form
    '''
    # username = None
    # password = None

    if request.method == "GET":
        return render_template('register.html')

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required"

        if user_exists(username):
            error = "Username already exists"

        if not password:
            error = "Password is required"


        if not validate_pass(password):
            error = "Password validation fail"
            entry = f"Log Entry failed login attempt: {datetime.now()} {username} {password} {jsonify({'ip', request.remote_addr})}"
            log.append(entry)
            print(entry)

        if error:
            flash(error)
            print("error:", error)
            return render_template('register.html')
            # return redirect(url_for("register"))

        with open("creds.txt", "a+") as f:
            print(username +" "+ sha256(password.encode()).hexdigest(), file=f)

        # return redirect(url_for("hello"))
        return redirect(url_for("login"))

@app.route('/login/', methods=['GET','POST'])
def login():
    '''
    Page prompts user to enter username/password into a form
    '''

    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if validate_creds(username, sha256(password.encode()).hexdigest()):

            authenticated_users.append(username)
            return redirect(url_for("home", current_user=username))
            # return render_template('home.html')
        else:
            error = "Invalid credentials"
            print("error:", error)

    if error:
        flash(error)
    #     return redirect(url_for("login"))
    # else:
    return render_template('login.html')

@app.route('/home/')
@app.route("/home/<current_user>")
def home(current_user=None):
    '''
    Home page after logging in
    '''
    if current_user and current_user in authenticated_users:
        return render_template('home.html', name=current_user)
    return redirect(url_for("login"))



# @app.route('/update/')
@app.route("/update/<current_user>" , methods=['GET','POST'])
def update(current_user=None):
    '''
    Update password for logged in user
    '''
    if request.method == "GET":
        if current_user and current_user in authenticated_users:
            return render_template('update.html')

    if request.method == "POST":
        if current_user and current_user in authenticated_users:
            username = request.form["username"]
            password = request.form["password"]
            error = None

            if not username:
                error = "Username is required"

            if not password:
                error = "Password is required"

            if not validate_pass(password):
                error = f"Password validation fail"

            if error:
                flash(error)
                print("error:", error)
            else:
                print("adding new password")
                with open("creds.txt", "a+") as f:
                    print(username +" "+ sha256(password.encode()).hexdigest(), file=f)

    return redirect(url_for("login"))


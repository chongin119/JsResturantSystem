from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app
from dbfunc import myDB

authBlue = Blueprint('authBlue',__name__,url_prefix='/auth')


@authBlue.route('/', methods = ["GET"])
def index():
    return redirect(url_for('authBlue.login'))

@authBlue.route('/login', methods = ["GET","POST"])
def login():
    return render_template('login.html')

@authBlue.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = myDB(current_app.config["DBPATH"])
        db.insertUser(username,password)
        del db

        return redirect(url_for('authBlue.login'))

    return render_template('register.html')


#webAPI below

@authBlue.route('/validUsername', methods = ["POST"])
def validUsername():
    db = myDB(current_app.config["DBPATH"])
    username = request.form.get('username')
    if username == "":
        del db
        return "null"

    if len(username) < 5:
        return "short"

    result = db.validUsername(username)
    print(result)
    del db
    if result:
        return "success"
    else:
        return "failure"


from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app

authBlue = Blueprint('authBlue',__name__,url_prefix='/auth')


@authBlue.route('/', methods = ["GET"])
def index():
    return redirect(url_for('authBlue.login'))

@authBlue.route('/login', methods = ["GET","POST"])
def login():
    return render_template('login.html')

@authBlue.route('/register', methods = ["GET","POST"])
def register():
    return render_template('register.html')


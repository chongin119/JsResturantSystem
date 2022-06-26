from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app

userBlue = Blueprint('userBlue',__name__,url_prefix='/user')

@userBlue.route('/')
def index():
    return "index"
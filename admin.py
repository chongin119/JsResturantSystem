from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint

adminBlue = Blueprint('adminBlue',__name__,url_prefix='/admin')

@adminBlue.route('/')
def index():
    return "index"
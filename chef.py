from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint

chefBlue = Blueprint('chefBlue',__name__,url_prefix='/chef')

@chefBlue.route('/')
def index():
    return "index"
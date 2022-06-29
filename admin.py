from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint


adminBlue = Blueprint('adminBlue',__name__,url_prefix='/admin')

@adminBlue.route('/', methods=["GET", 'POST'])
def index():
    return render_template('originalAdmin.html')

@adminBlue.route('/usermanage', methods=['GET', 'POST'])
def usermanage():
    if request.method == 'GET':
        return render_template('adminManage.html')
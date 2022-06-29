from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app
from dbfunc import myDB
from ENDE import myAES

adminBlue = Blueprint('adminBlue',__name__,url_prefix='/admin')

@adminBlue.route('/', methods=["GET", 'POST'])
def index():
    return render_template('originalAdmin.html')

@adminBlue.route('/usermanage', methods=['GET', 'POST'])
def usermanage():
    db = myDB(current_app.config['DBPATH'])
    info = db.checkmenu()
    length = len(info['foodpic'])
    data = []
    for i in range(0, length):
        data.append([info['id'][i], info['foodpic'][i], info['name'][i], info['price'][i], info['sellplace'][i]])
    return render_template('adminManage.html', data = data)
    
@adminBlue.route('/deletemenu', methods=['GET', 'POST'])
def delete_menu():
    db = myDB(current_app.config['DBPATH'])
    if request.method == 'POST':
        id = request.form.get('id')
        print(id)
        db.deletemenu(id)
        del db
    return redirect(url_for('adminBlue.usermanage'))

@adminBlue.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    return render_template('addproduct.html')

# @adminBlue.route('/addproduct/addmenu', methods=['GET', 'POST'])
# def add_menu():
    # if request.method == 'POST':

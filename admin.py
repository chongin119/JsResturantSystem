from email.mime import base
from unicodedata import category
from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app, jsonify
from dbfunc import myDB
from ENDE import myAES
import base64

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
def addproduct():
    return render_template('addproduct.html')

@adminBlue.route('/addmenu', methods=['GET', 'POST'])
def addmenu():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = ''.join(request.values.getlist('radio_catergory'))
        file = request.files.get('file')
        encoded = base64.b64encode(file.read())
        foodpic = str(encoded, 'utf-8')
        canteen = ''.join(request.values.getlist('canteen'))
        print(name, price, foodpic, canteen, category)
        db = myDB(current_app.config['DBPATH'])
        db.addmenu(name, price, foodpic, canteen, category)
        del db
        return redirect(url_for('adminBlue.addproduct'))

    return render_template('addproduct.html')

from email.mime import base
from pydoc import describe
from unicodedata import category
from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app, jsonify
from dbfunc import myDB
from ENDE import myAES
import base64

adminBlue = Blueprint('adminBlue',__name__,url_prefix='/admin')

@adminBlue.route('/logout',methods=["POST"])
def logout():
    del session['username']
    return url_for('authBlue.login')

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
def deletemenu():
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

@adminBlue.route('/orderindex', methods=['GET', 'POST'])
def orderindex():
    return render_template('OrderManage.html')

@adminBlue.route('/ordermanage', methods=['GET', 'POST'])
def ordermanage():
    db = myDB(current_app.config['DBPATH'])
    info = db.ordermanage()
    length = len(info['id'])
    data = []
    num = []
    name = []
    for i in range(0, length):
        list = info['list'][i].split(';')
        decode = list[:-1]
        num1 = []
        name1 = []
        for j in range(0, len(decode)):
            order = decode[j].split('_')
            print(order)
            num1.append(order[0])
            name1.append(order[1])
        num.append(num1)
        name.append(name1)
    detail = []

    for i in range(0, len(num)):
        detail1 = []
        for j in range(0, len(num[i])):
            info = db.listdetail(num[i][j], int(name[i][j]))
            detail1.append(info)
        detail.append(detail1)
    
    describe = []
    for i in range(0, len(detail)):
        describe.append(','.join(detail[i]))
    print(describe)

    for i in range(0, length):
        data.append([info['id'][i], info['date'][i], info['name'][i], describe[i], info['sum'][i], info['comment'][i], info['status'][i]])
    return render_template('OrderManage.html', data = data)



from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint,current_app,jsonify
import json
from dbfunc import myDB

chefBlue = Blueprint('chefBlue',__name__,url_prefix='/chef')

@chefBlue.route('/chefMain',methods=["GET"])
def chefMain():
    username = session["username"]
    navComponent = {"1":["处理订单",True,"/chef/chefMain"]}

    db = myDB(current_app.config["DBPATH"])

    del db

    return render_template('chefMain.html',
                            username = username,
                            navComponent = navComponent, )

#webAPI below

@chefBlue.route('/logout',methods=["POST"])
def logout():
    del session['username']
    return url_for('authBlue.login')

@chefBlue.route('/getHistoryOrder',methods = ["POST"])
def getHistoryOrder():
    jsonstring = request.json
    offset = jsonstring["pageNumber"]
    Size = jsonstring["pageSize"]
    username = session["username"]
    db = myDB(current_app.config['DBPATH'])
    info = db.getHistoryOrderChef(username,offset)
    del db
    #print(info)
    return jsonify(info)

@chefBlue.route('/finishOrder',methods = ["POST"])
def finishOrder():
    id = request.form.get('id')
    db = myDB(current_app.config["DBPATH"])
    db.finishOrder(id)
    db.updateExpAndPoint(id)
    del db
    return jsonify('aaa')
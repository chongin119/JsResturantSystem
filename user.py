from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app
from sqlalchemy import true

from dbfunc import myDB

userBlue = Blueprint('userBlue',__name__,url_prefix='/user')

@userBlue.route('/userOrder')
def userOrder():
    username = session["username"]
    navComponent = {"1":["用户订餐",True],"2":["查询过去订单",False],"3":["更改个人资料",False]}

    db = myDB(current_app.config["DBPATH"])
    pics = db.randomChoosePic()


    return render_template('userOrder.html', 
                            username = username, 
                            navComponent = navComponent, 
                            pics = pics, 
                            picslen = len(pics))
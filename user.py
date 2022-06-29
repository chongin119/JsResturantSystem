from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app, jsonify
from sqlalchemy import true

from dbfunc import myDB

userBlue = Blueprint('userBlue',__name__,url_prefix='/user')

@userBlue.route('/userOrder',methods=["GET"])
def userOrder():
    username = session["username"]
    navComponent = {"1":["用户订餐",True,"/user/userOrder"],"2":["查询过去订单",False],"3":["更改个人资料",False]}

    db = myDB(current_app.config["DBPATH"])
    pics = db.randomChoosePic()
    resturants = db.getResturant()
    categorys = db.getCategorys()
    del db 

    return render_template('userOrder.html', 
                            username = username, 
                            navComponent = navComponent, 
                            pics = pics, 
                            picslen = len(pics),
                            resturants = resturants,
                            categorys = categorys)

#webAPI below
@userBlue.route('/getFoodCard',methods=["POST"])
def getFoodCard():

    needCategoryItems = request.form.items()
    needCategory = {}
    resturantId = ""
    for item in needCategoryItems:

        if item[0] != "resturantId":
            #num = item[0][item[0].find('[') + 1 : item[0].find(']')]
            needCategory[item[0]] = item[1]
        else:
            resturantId = item[1]

    #print(needCategory)
    needCategory = [key for key in needCategory if needCategory[key] != 'false']

    db = myDB(current_app.config["DBPATH"])
    foods = db.getFoodCard(needCategory,resturantId)
    del db
    if len(foods) > 10:
        foods = foods[0:10]
    totalpage = len(foods) // 10
    if totalpage == 0: totalpage = 1

    resp = {"foods":foods,"totalpage":totalpage}
    return jsonify(resp)
from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint, current_app, jsonify
from sqlalchemy import true
import json

from dbfunc import myDB

userBlue = Blueprint('userBlue',__name__,url_prefix='/user')

@userBlue.route('/userOrder',methods=["GET"])
def userOrder():
    username = session["username"]
    navComponent = {"1":["用户订餐",True,"/user/userOrder"],"2":["查询过去订单",False,"/user/userHistory"],"3":["更改个人资料",False]}

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

@userBlue.route('/userHistory',methods=["GET"])
def userHistory():
    username = session["username"]
    navComponent = {"1":["用户订餐",False,"/user/userOrder"],"2":["查询过去订单",True,"/user/userHistory"],"3":["更改个人资料",False]}

    db = myDB(current_app.config["DBPATH"])

    del db

    return render_template('userHistory.html',
                            username = username,
                            navComponent = navComponent,)

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


    totalpage = len(foods) // 10 + 1
    if len(foods) > 10:
        foods = foods[0:10]

    resp = {"foods":foods,"totalpage":totalpage}
    return jsonify(resp)

@userBlue.route('/getFoodCardHvPages',methods=["POST"])
def getFoodCardHvPages():
    jsonDict = request.json
    #print(jsonDict)
    offset = jsonDict["pageNumber"]
    Size = jsonDict["pageSize"]
    data = json.loads(jsonDict["data"])

    resturantId = data["resturantId"]
    needCategory = data["categoryIds"]

    needCategory = [key for key in needCategory if needCategory[key] != False]

    db = myDB(current_app.config["DBPATH"])
    foods = db.getFoodCard(needCategory,resturantId)
    del db

    totalpage = len(foods)
    resp = {"total":totalpage,"rows":foods[offset:offset+10]}

    return jsonify(resp)

@userBlue.route('/getFoodCardHvPage',methods=["POST"])
def getFoodCardHvPage():

    needCategoryItems = request.form.items()
    needCategory = {}
    resturantId = ""
    curPage = 0
    for item in needCategoryItems:
        if item[0] == "resturantId":
            resturantId = item[1]
        elif item[0] == "curPage":
            curPage = int(item[1])
        else:
            #num = item[0][item[0].find('[') + 1 : item[0].find(']')]
            needCategory[item[0]] = item[1]



    needCategory = [key for key in needCategory if needCategory[key] != 'false']

    db = myDB(current_app.config["DBPATH"])
    foods = db.getFoodCard(needCategory,resturantId)
    del db

    totalpage = len(foods) // 10 + 1
    if len(foods) > 10:
        foods = foods[(curPage - 1) * 10 : 10 + (curPage - 1) * 10]

    resp = {"foods":foods,"totalpage":totalpage}
    return jsonify(resp)

@userBlue.route('/getFoodPic',methods=["POST"])
def getFoodPic():
    id = request.form.get('id')
    db = myDB(current_app.config["DBPATH"])
    pic = db.getFoodPic(id)
    del db
    return pic

@userBlue.route('/getCarSession',methods = ["POST"])
def getCarSession():

    try:
        #del session["myCar"]
        string = session["myCar"]
    except:
        string = "{}"
    return jsonify(string)

@userBlue.route('/setCarSession',methods = ["POST"])
def setCarSession():
    string = request.form.get('string')
    session["myCar"] = string
    return jsonify(session["myCar"])

@userBlue.route('/getCarLst',methods = ["POST"])
def getCarLst():
    carLst = request.form.items()
    carDict = {}

    for item in carLst:
        carDict[item[0]] = item[1]
    db = myDB(current_app.config["DBPATH"])
    result = {}
    for i in carDict:
        info = db.getCarLst(i,carDict[i])
        if result.get(info[2]) != None:
            result[info[2]].append({"name":info[0],"price":info[1],"count":info[3],"foodId": info[4]})
        else:
            result[info[2]] = [{"name":info[0],"price":info[1],"count":info[3],"foodId": info[4]}]

    #print(result)
    del db
    return jsonify(result)

@userBlue.route('/createOrder',methods = ["POST"])
def createOrder():
    info = request.json
    print(info)
    comment = info[1]
    info = info[0]
    print(info,comment)
    username = session["username"]
    db = myDB(current_app.config["DBPATH"])
    infoDict = {}
    for i in info:
        foodstr = ""
        sumOfPrice = 0.0

        for j in info[i]:
            foodstr += j['foodId'] + '_' + j['count'] + ';'
            sumOfPrice += int(j['count']) * j['price']
        db.createOrder(foodstr,sumOfPrice,username,comment)
    del db
    del session["myCar"]
    return jsonify("Aaa")

@userBlue.route('/changeSession',methods = ["POST"])
def changeSession():
    string = session["myCar"]
    id = request.form.get('id')
    jsonDict = json.loads(string)


    temp = jsonDict[id] - 1
    if temp == 0:
        del jsonDict[id]
    else:
        jsonDict[id] = temp

    session["myCar"] = json.dumps(jsonDict)
    return jsonify('aaa')
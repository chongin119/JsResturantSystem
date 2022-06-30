import sqlite3 as s3
from ENDE import myAES
import os.path
import random
from datetime import datetime

class myDB():
    def __init__(self,path):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, path)
        self.db = s3.connect(db_path)
        self.c = self.db.cursor()
        
    def __del__(self):
        self.db.close()
    
    #query
    def validUsername(self,username):
        info = self.c.execute("""SELECT username FROM userInfo WHERE username == ?""",(username,)).fetchone()
        if info != None:
            return False
        return True

    def validLogin(self,username,password,op):
        info = self.c.execute("""SELECT username,password,permission FROM userInfo WHERE username == ?""",(username,)).fetchone()
        if info == None:
            return False
        
        operator = myAES(op)
        validPassword = operator.decrypt(info[1])
        
        if validPassword != password:
            return False
        return {"username":info[0],"permission":info[2]}

    #随机展示三张图片
    def randomChoosePic(self):
        idss = self.c.execute("""SELECT id FROM food""").fetchall()
        ids = []
        for i in idss:
            ids.append(i[0])

        idLen = len(ids)
        
        if idLen > 3:
            randomLst = random.sample(ids,3)
        else:
            randomLst = ids
        pics = {}
        for cnt, i in enumerate(randomLst):
            picBlob = self.c.execute("""SELECT 
                                        f.foodPic,f.name,r.name 
                                        FROM 
                                        food AS f LEFT JOIN resturant AS r 
                                        ON f.sellFrom == r.id 
                                        WHERE f.id == ?""",(i,)).fetchone()
            pics[cnt] = picBlob

        return pics 

    #获取所有餐厅
    def getResturant(self):
        Resturants = self.c.execute("""SELECT id,name FROM resturant""").fetchall()
        resturants = {}
        resturants[0] = {"id": "0",
                         "name": "全部"}
        for cnt, i in enumerate(Resturants):
            resturants[cnt+1] = {"id":i[0],
                                "name":i[1]}

        return resturants

    #获取所有食品类别
    def getCategorys(self):
        Categorys = self.c.execute("""SELECT id,name FROM category""").fetchall()
        categorys = {}

        for cnt, i in enumerate(Categorys):
            categorys[cnt+1] = {"id" : i[0],
                                "name" : i[1]}
        return categorys

    #获取所有食物(通过食堂和类别)
    def getFoodCard(self,category, resturantId,sortOrder):
        #print(category)
        if len(category) == 0:#没有选等于全选
            categorys = self.c.execute("""SELECT id FROM category""").fetchall()
            for i in categorys:
                category.append(i[0])

        foods = []
        #print(category)
        if resturantId == '0':
            for i in category:
                tempFood = self.c.execute("""SELECT f.id,f.name,f.price,r.name FROM food AS f LEFT JOIN resturant AS r
                                            ON f.sellFrom == r.id
                                            WHERE f.category == ? ORDER By f.id""",(i,)).fetchall()
                for j in tempFood:
                    foods.append({'id':j[0],'name':j[1],'price':j[2],'rName':j[3]})
        else:
            for i in category:
                tempFood = self.c.execute("""SELECT f.id,f.name,f.price,r.name FROM food AS F LEFT JOIN resturant AS r 
                                            ON f.sellFrom == r.id
                                            WHERE f.category == ? and f.sellFrom == ? ORDER By f.id""",(i,resturantId)).fetchall()
                for j in tempFood:
                    foods.append({'id':j[0],'name':j[1],'price':j[2],'rName':j[3]})
        print(sortOrder)
        if sortOrder == None:
            foods.sort(key = lambda x:x['id'])
        else:
            if sortOrder == 'desc': rr = True
            else:rr = False
            foods.sort(key = lambda x:x['price'],reverse=rr)
        return foods

    #获取食物视图By Id
    def getFoodPic(self,id):
        pic = self.c.execute("""SELECT foodPic FROM food WHERE id == ?""",(id,)).fetchone()[0]

        return pic

    #获取购物车货物
    def getCarLst(self,id,count):
        result = self.c.execute("""SELECT f.name,f.price,r.name 
                                    FROM food AS f LEFT JOIN resturant AS r 
                                    ON f.sellFrom == r.id 
                                    WHERE f.id == ?""",(id,)).fetchone()
        result = list(result)
        result.append(count)
        result.append(id)
        return result

    #获取userId by username
    def getUserIdByUsername(self,username):
        id = self.c.execute("""SELECT id FROM userInfo WHERE username == ?""",(username,)).fetchone()[0]
        return id

    #获取食物名字byId
    def getFoodNameById(self,id):
        name = self.c.execute("""SELECT name FROM food WHERE id == ?""",(id,)).fetchone()
        if name == None:
            return "已被删除"
        return name[0]

    #获取餐厅名字byFoodId
    def getResturantNameByFoodId(self,foodId):
        name = self.c.execute("""SELECT r.name 
                                FROM food AS f LEFT JOIN resturant AS r 
                                ON f.sellFrom == r.id
                                WHERE f.id == ?""",(foodId,)).fetchone()

        if name == None:
            return "已被删除"
        return name[0]

    # 获取餐厅IdbyFoodId
    def getResturantIdByFoodId(self, foodId):
        name = self.c.execute("""SELECT r.id
                                FROM food AS f LEFT JOIN resturant AS r 
                                ON f.sellFrom == r.id
                                WHERE f.id == ?""", (foodId,)).fetchone()

        if name == None:
            return "已被删除"
        return name[0]

    #获取某用户所有订单
    def getHistoryOrder(self,username,offset):
        userId = self.getUserIdByUsername(username)
        info = self.c.execute("""SELECT id,orderFoodId,time, comment,sumOfPrice,status FROM orderTable WHERE fromUser == ? ORDER BY id DESC""",(userId,)).fetchall()

        if info == []:
            return {"total":0}

        result = []
        total = len(info)
        #print(info)
        for i in info:
            tempDict = {"id":i[0],"time":i[2],"comment":i[3],"sumOfPrice":i[4],"status":i[5]}
            content = ""
            food = i[1].split(';')
            resturant = self.c.execute("""SELECT r.name FROM orderTable AS o
                                            LEFT JOIN resturant AS r 
                                            ON o.sellFrom == r.id WHERE sellFrom == ? """,(i[0],)).fetchone()
            if resturant  == None:
                resturant = ""
            else:
                resturant = resturant[0]

            for cnt, j in enumerate(food):
                if cnt == len(food) - 1:
                    break
                temp = j.split('_')
                #print(temp[0])
                name = self.getFoodNameById(temp[0])
                content += f"{name} x{temp[1]}<br>"

                if resturant == "" or resturant == "已被删除":
                    resturant = self.getResturantNameByFoodId(temp[0])

            tempDict["orderFood"] = content
            tempDict["resturant"] = resturant
            result.append(tempDict)

        result = result[offset:offset+10]
        return {"total":total,"rows":result}

    # 获取某负责人未完成订单
    def getHistoryOrderChef(self, username, offset):
        userId = self.getUserIdByUsername(username)
        ownRest = self.c.execute("""SELECT r.id FROM resturant AS r LEFT JOIN userInfo as u ON r.operator == u.id WHERE u.id == ?""",(userId,)).fetchone()[0]
        print(ownRest)
        info = self.c.execute(
            """SELECT id,orderFoodId,time, comment,sumOfPrice,status FROM orderTable WHERE sellFrom == ? and status == ?""",
            (ownRest,0)).fetchall()

        if info == []:
            return {"total": 0}

        result = []
        total = len(info)
        # print(info)
        for i in info:
            tempDict = {"id": i[0], "time": i[2], "comment": i[3], "sumOfPrice": i[4], "status": i[5]}
            content = ""
            food = i[1].split(';')

            resturant = self.c.execute("""SELECT r.name FROM orderTable AS o
                                                        LEFT JOIN resturant AS r 
                                                        ON o.sellFrom == r.id WHERE sellFrom == ? """,
                                       (ownRest,)).fetchone()
            if resturant == None:
                resturant = ""
            else:
                resturant = resturant[0]

            for cnt, j in enumerate(food):
                if cnt == len(food) - 1:
                    break
                temp = j.split('_')
                # print(temp[0])
                name = self.getFoodNameById(temp[0])
                content += f"{name} x{temp[1]}<br>"

                if resturant == "" or resturant == "已被删除":
                    resturant = self.getResturantNameByFoodId(temp[0])

            tempDict["orderFood"] = content
            tempDict["resturant"] = resturant
            result.append(tempDict)

        result = result[offset:offset + 10]
        return {"total": total, "rows": result}

    #获取用户资讯
    def getProfile(self,username):
        userId = self.getUserIdByUsername(username)
        info = self.c.execute("""SELECT username,profilePhoto,email,phoneNum FROM userInfo WHERE id == ?""",(userId,)).fetchone()
        infoDict = {"username":info[0],"profilePhoto":info[1],"email":info[2],"phoneNum":info[3]}
        return infoDict

    #獲取用戶是否有頭象
    def hvProfilePic(self,username):

        userId = self.getUserIdByUsername(username)
        judge = self.c.execute("""SELECT profilePhoto FROM userInfo WHERE id == ?""",(userId,)).fetchone()

        if judge != None:
            return judge[0]
        return False

    #获取用户权限
    def getPermissionByUsername(self,username):
        userId = self.getUserIdByUsername(username)
        permission = self.c.execute("""SELECT permission FROM userInfo WHERE id == ?""",(userId,)).fetchone()[0]
        return permission

    #insert del update
    def insertUser(self,username,password):
        id = self.c.execute("""SELECT id FROM userInfo ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO userInfo (id,username,password,profilePhoto,email,phoneNum,permission) VALUES (?,?,?,?,?,?,?)""",(id,username,password,None,None,None,2))

        self.db.commit()

    def createOrder(self,foodIds,sumOfPrice,username,comment,resturantId):
        id = self.c.execute("""SELECT id FROM orderTable ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        userId = self.getUserIdByUsername(username)
        t =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.c.execute("""INSERT INTO orderTable (id, orderFoodId, fromUser, time, comment, sumOfPrice, status, sellFrom) VALUES (?,?,?,?,?,?,?,?)
                        """,(id, foodIds, userId, t, comment, sumOfPrice, 0, resturantId))
        self.db.commit()

    #完成订单
    def finishOrder(self,id):
        self.c.execute("""UPDATE orderTable SET status = ? WHERE id == ?""",(1,id));
        self.db.commit()

    #更改用戶資訊
    def changeProfile(self,username,email,phone,profilePic):
        userId = self.getUserIdByUsername(username)

        self.c.execute("""UPDATE userInfo SET profilePhoto = ?, email = ?, phoneNum = ? WHERE id == ?""",(profilePic, email, phone, userId))
        self.db.commit()

#我是分隔线------------------------------------------------------------

    #check the menu
    def checkmenu(self):
        info = self.c.execute("""SELECT id, foodPic, name, price FROM food""").fetchall()
        sellform = self.c.execute("""SELECT resturant.name FROM food INNER JOIN resturant WHERE food.sellFrom = resturant.id""").fetchall()
        id = []
        foodpic = []
        name = []
        price = []
        sellplace = []

        length = len(info)
        for i in range(0, length):
            id.append(info[i][0])
            foodpic.append(info[i][1])
            name.append(info[i][2])
            price.append(info[i][3])
            sellplace.append(sellform[i][0])
        return {'id': id, 'foodpic': foodpic, 'name': name, 'price': price, 'sellplace': sellplace}

    #delete the menu
    def deletemenu(self, id):
        self.c.execute("""DELETE FROM food WHERE id=?""",id)

        self.db.commit()
     
    #add the product into the menu
    def addmenu(self, name, price, foodpic, canteen, category):
        id = self.c.execute("""SELECT id FROM food ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1
        self.c.execute("""INSERT INTO food(id, name, price, foodPic, sellFrom, category) VALUES (?,?,?,?,?,?)""", (id, name, price, foodpic, canteen, category))
        self.db.commit()
    
    #get the ordertable
    def ordermanage(self):
        info = self.c.execute("""SELECT id, time, orderFoodId, sumOfPrice, comment, status FROM orderTable""").fetchall()
        username = self.c.execute("""SELECT userInfo.username FROM orderTable INNER JOIN userInfo WHERE orderTable.fromUser = userInfo.id""").fetchall()

        id = []
        date = []
        name = []
        list = []
        sum = []
        comment = []
        status = []

        length = len(info)
        for i in range(0, length):
            id.append(info[i][0])
            date.append(info[i][1])
            name.append(username[i][0])
            list.append(info[i][2])
            sum.append(info[i][3])
            comment.append(info[i][4])
            status.append(info[i][5])
        
        return {'id': id, 'date': date, 'name': name, 'list': list, 'sum': sum, 'comment': comment, 'status': status}

    # get the detail
    def listdetail(self, num, name):
        print("name is", type(name))
        choose = self.c.execute("""SELECT name FROM food WHERE id=?""",(name,)).fetchone()[0]
        if choose == None:
            detail = "该菜品已经售光了"
        detail = choose + '*' + num
        return detail

if __name__ == '__main__':
    db = myDB('./web.db')
    del db

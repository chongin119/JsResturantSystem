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
    def getFoodCard(self,category, resturantId):
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
    #insert del update
    def insertUser(self,username,password):
        id = self.c.execute("""SELECT id FROM userInfo ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO userInfo (id,username,password,profilePhoto,email,phoneNum,permission) VALUES (?,?,?,?,?,?,?)""",(id,username,password,None,None,None,2))

        self.db.commit()

    def createOrder(self,foodIds,sumOfPrice,username,comment):
        id = self.c.execute("""SELECT id FROM orderTable ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        userId = self.getUserIdByUsername(username)
        t =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.c.execute("""INSERT INTO orderTable (id, orderFoodId, fromUser, time, comment, sumOfPrice, status) VALUES (?,?,?,?,?,?,?)
                        """,(id, foodIds, userId, t, comment, sumOfPrice, 0))
        self.db.commit()


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
        self.c.execute("""DELETE FROM food WHERE id={}""".format(id))

        self.db.commit() 

if __name__ == '__main__':
    db = myDB('./web.db')
    del db

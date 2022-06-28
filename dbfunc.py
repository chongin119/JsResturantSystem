import sqlite3 as s3
from ENDE import myAES

class myDB():
    def __init__(self,path):
        self.db = s3.connect(path)
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

    #insert del update
    def insertUser(self,username,password):
        id = self.c.execute("""SELECT id FROM userInfo ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO userInfo (id,username,password,permission) VALUES (?,?,?,?)""",(id,username,password,2))

        self.db.commit()

if __name__ == '__main__':
    db = myDB('./web.db')
    del db

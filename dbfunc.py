import sqlite3 as s3

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

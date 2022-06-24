import sqlite3 as s3

class myDB():
    def __init__(self,path):
        self.db = s3.connect(path)
        
    def __del__(self):
        self.db.close()
        

if __name__ == '__main__':
    db = myDB('./web.db')
    del db

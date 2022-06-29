import base64
import io
from dbfunc import myDB

if __name__ == '__main__':
    path = '2.jpg'
    id = 11
    db = myDB('web.db')
    with open(path,'rb') as f:
        
        encoded = base64.b64encode(f.read())
        encoded = str(encoded,'utf-8')

        db.c.execute("""UPDATE food SET foodPic == ? WHERE id == ?""",(encoded,id))
        db.db.commit()
    
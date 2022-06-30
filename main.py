from flask import Flask, request, redirect, render_template, session, url_for, current_app
from flask import Blueprint
from admin import adminBlue
from auth import authBlue
from user import userBlue
from chef import chefBlue
from dbfunc import myDB

web = Flask(__name__)
web.register_blueprint(adminBlue)
web.register_blueprint(authBlue)
web.register_blueprint(userBlue)
web.register_blueprint(chefBlue)
web.config.from_pyfile('config.py')

#对非法访问和登入进行检测
@web.before_request
def check():
    if request.method == "POST":
        pass
    elif not request.path.startswith('/static'):
        if session.get('username') == None:
            if request.path.startswith('/auth') or request.path == '/':
                pass
            else:
                return redirect(url_for('authBlue.login'))
        else:
            db = myDB(current_app.config["DBPATH"])
            permission = db.getPermissionByUsername(session["username"])
            del db
            if request.path.startswith('/auth') or request.path == '/':
                if permission == 0:
                    return redirect(url_for('adminBlue.index'))
                if permission == 1:
                    return redirect(url_for('chefBlue.chefMain'))
                if permission == 2:
                    return redirect(url_for('userBlue.userOrder'))
            else:
                if request.path.startswith('/user'):
                    if permission == 2:
                        pass
                    else:
                        if permission == 0:
                            return redirect(url_for('adminBlue.index'))
                        if permission == 1:
                            return redirect(url_for('chefBlue.chefMain'))
                elif request.path.startswith('/admin'):
                    if permission == 0:
                        pass
                    else:
                        if permission == 1:
                            return redirect(url_for('chefBlue.chefMain'))
                        if permission == 2:
                            return redirect(url_for('userBlue.userOrder'))
                elif request.path.startswith('/chef'):
                    if permission == 1:
                        pass
                    else:
                        if permission == 0:
                            return redirect(url_for('adminBlue.index'))
                        if permission == 2:
                            return redirect(url_for('userBlue.userOrder'))

@web.route('/')
def nothing():
    return redirect('/auth/')


if __name__ == '__main__':
    web.run(port = 8000, debug = True)
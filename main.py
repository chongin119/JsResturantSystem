from flask import Flask, request, redirect, render_template, session, url_for
from flask import Blueprint
from admin import adminBlue
from auth import authBlue
from user import userBlue
from chef import chefBlue


web = Flask(__name__)
web.register_blueprint(adminBlue)
web.register_blueprint(authBlue)
web.register_blueprint(userBlue)
web.register_blueprint(chefBlue)
web.config.from_pyfile('config.py')

#remember to add before request

@web.route('/')
def nothing():
    return redirect('/auth/')


if __name__ == '__main__':
    web.run(port = 8000, debug = True)
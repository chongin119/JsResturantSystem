from flask import Flask, request, redirect, render_template, session, url_for

web = Flask(__name__)

web.config['dbPath'] = './web.db'


@web.route('/', methods = ["GET"])
def index():
    return redirect(url_for('login'))

@web.route('/login', methods = ["GET","POST"])
def login():
    return render_template('login.html')

@web.route('/register', methods = ["GET","POST"])
def register():
    return render_template('register.html')



if __name__ == '__main__':
    web.run(port = 8000, debug = True)
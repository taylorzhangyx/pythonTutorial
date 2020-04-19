from application import app
from flask import render_template


user = {}
user["login"] = False
user["language"] = 'eng'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', **user)


@app.route('/classes', methods=['GET'])
def classes():
    return render_template('classes.html', login=True)


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html', login=True)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', login=True)


from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    header = '<h1> first page i like to tell you </h1>'
    return header

from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restx import Api

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)
db = MongoEngine(app)


from application import routes

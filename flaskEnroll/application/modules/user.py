from application import db


class User(db.Document):
    userId = db.IntField(unique=True)
    firstName = db.StringField(max_length=20)
    password = db.StringField()
    email = db.StringField()

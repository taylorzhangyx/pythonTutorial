from application import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Document):
    userId = db.IntField(unique=True)
    firstName = db.StringField(max_length=20)
    lastName = db.StringField(max_length=20)
    password = db.StringField()
    email = db.StringField(unique=True)

    def get_password(self, password):
        print("password getter is called!")
        self.password = check_password_hash(password)

    def check_password(self, password):
        print("password validator is called!")
        self.password = generate_password_hash(password)

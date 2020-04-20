from application import db


class Course(db.Document):
    courseId = db.IntField(unique=True)
    title = db.StringField()
    description = db.StringField(max_length=512)
    credits = db.IntField()
    term = db.StringField()

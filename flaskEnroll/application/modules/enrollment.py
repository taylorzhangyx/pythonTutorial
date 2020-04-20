from application import db


class Enrollment(db.Document):
    userId = db.IntField()
    courseId = db.IntField()

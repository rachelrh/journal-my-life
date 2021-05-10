from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    posts = db.relationship("Post")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "posts": [p.serialize() for p in self.posts]
        }

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String, nullable = False)
    pictures = db.Column(db.String, nullable=True)
    entry = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, **kwargs):
        self.date = kwargs.get("date")
        self.location = kwargs.get("location")
        self.pictures = kwargs.get("pictures")
        self.entry = kwargs.get("entry")
        self.user_id = kwargs.get("user_id")
    

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "location": self.location,
            "pictures": self.pictures,
            "entry": self.entry,
            "user_id": self.user_id
        }
    
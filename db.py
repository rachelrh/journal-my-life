from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String, nullable = False)
    pictures = db.Column(db.String, nullable=True)
    entry = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.date = kwargs.get("date")
        self.location = kwargs.get("location")
        self.pictures = kwargs.get("pictures")
        self.entry = kwargs.get("entry")
    

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "location": self.location,
            "pictures": self.pictures,
            "entry": self.entry
        }
    
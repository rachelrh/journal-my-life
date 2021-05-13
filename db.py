from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import base64
import boto3    #interator w amazon aws bucket
from io import BytesIO  #convert things into byte string
from mimetypes import guess_extension, guess_type #figure out what type file (ex: jpg, png)
from PIL import Image #image handling library
import random
import re
import string

import bcrypt

db = SQLAlchemy()

EXTENSIONS = ['png', 'gif', 'jpg', 'jpeg']

BASE_DIR = os.getcwd()
S3_BUCKET = 'journalmylifebucket'
S3_BASE_URL = f'https://{S3_BUCKET}.s3-us-east-2.amazonaws.com'

class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String, nullable=False)
    salt = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, **kwargs):
        self.create(kwargs.get('image_data'))
        self.post_id = kwargs.get('post_id')

    def serialize(self):
        return {
            "id": self.id,
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "created_at": str(self.created_at)
        }

    def create(self, image_data):
        try:
            ext = guess_extension(guess_type(image_data)[0])[1:]
            if ext not in EXTENSIONS:
                raise Exception(f"Extention {ext} not supported")
            salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(16))
            img_str = re.sub("^data:image/.+;base64,", "", image_data)
            img_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_data))
            self.base_url = S3_BASE_URL
            self.salt = salt
            self.extension = ext
            self.height = img.height
            self.width = img.width
            self.created_at = datetime.datetime.now()
            img_filename = f"{salt}.{ext}"
            self.upload(img, img_filename)

        except Exception as e:
            print("Error:", e)

    def upload(self, img, img_filename):
        try:
            img_temploc = f'{BASE_DIR}/{img_filename}'
            img.save(img_temploc)
            s3_client = boto3.client('s3')
            s3_client.upload_file(img_temploc, S3_BUCKET, img_filename)

            s3_resource = boto3.resource('s3')     
            object_acl = s3_resource.ObjectAcl(S3_BUCKET, img_filename)
            object_acl.put(ACL='public-read')
            os.remove(img_temploc)
            
        except Exception as e:
            print('Upload Failed:', e)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)
    posts = db.relationship("Post", cascade="delete")

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()
    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)
    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration
    def verify_update_token(self, update_token):
       return update_token == self.update_token
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "posts": [p.serialize() for p in self.posts]
        }

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable = False)
    entry = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship("Asset", cascade="delete")

    def __init__(self, **kwargs):
        self.year = kwargs.get('year')
        self.month = kwargs.get('month')
        self.day = kwargs.get('day')
        self.location = kwargs.get("location")
        self.entry = kwargs.get("entry")
        self.user_id = kwargs.get("user_id")
    

    def serialize(self):
        return {
            "id": self.id,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "location": self.location,
            "entry": self.entry,
            "user_id": self.user_id,
            "images": [i.serialize() for i in self.images]
        }
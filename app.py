import json
import os
from db import db
from db import Post, User, Asset
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "posts.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


# your routes here

@app.route("/api/users/<int:user_id>/")
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body.get('name')
    username = body.get('username')
    if username is None:
        return failure_response("No username provided")
    if name is None:
        return failure_response("No name provided")
    new_user = User(name=name, username=username)

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize())

@app.route("/api/users/<int:user_id>/posts/")
def get_all_posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response([p.serialize() for p in user.posts])

@app.route("/api/users/<int:user_id>/posts/<int:year>/<int:month>/<int:day>/")
def get_post_by_date(user_id, year, month, day):

    #iso8601
    #datetime.isoformat 
    #year, month, day
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    
    #existing = User.query.join(User.spaces).filter(User.username=='Bob', Space.name=='Mainspace').first()
    posts = User.query.join(User.posts).filter(Post.year==year, Post.month==month, Post.day==day).all()
    posts = User.query.filter_by(year=year).filter_by(month=month).filter_by(day=day).all()
    return success_response([p.serialize() for p in posts])

@app.route("/api/users/<int:user_id>/posts/", methods=["POST"])
def create_post(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    body = json.loads(request.data)
    year = json.loads('year')
    month = json.loads('month')
    day = json.loads('day')
    location = body.get('location')
    pictures = body.get('pictures')
    entry = body.get('entry')
    if year is None or month is None or day is None:
        return failure_response("Invalid date provided")
    if location is None:
        return failure_response("No location provided")
    if entry is None:
        return failure_response("No entry provided")
    new_post = Post(year=year, month=month, day=day, location=location, pictures=pictures, entry=entry, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize())


@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(user_id, post_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    posts = user.posts
    p = None
    if posts == []:
        return failure_response('Post not found!')
    for post in posts:
        if post.id == post_id:
            p = post
            db.session.delete(p)
    if p is None:
        return failure_response('Post not found!')
    db.session.commit()
    return success_response(p.serialize())


@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods=["POST"])
def update_post(user_id, post_id):
    pass

@app.route("/api/users/<int:user_id>/posts/<int:post_id>/upload/", methods=['POST'])
def upload(user_id, post_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    # post w post_id is in user.posts
    posts = user.posts
    if posts == []:
        return failure_response('Post not found!')

    body = json.loads(request.data)
    image_data = body.get('image_data')
    if image_data is None:
        return failure_response('No image provided')
    asset = Asset(image_data=image_data, post_id=post_id)
    db.session.add(asset)
    db.session.commit()
    return success_response(asset.serialize(), 201)

#@app.route("")
# img link or img id in json req body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=True)
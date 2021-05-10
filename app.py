import json
import os
from db import db
from db import Post, User
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
    if name is None:
        return failure_response("No name provided")
    new_user = User(name=name)

    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize())

@app.route("/api/users/<int:user_id>/posts/")
def get_all_posts(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response([p.serialize() for p in user.posts])

@app.route("/api/users/<int:user_id>/posts/<int:post_date>/")
def get_post_by_date(user_id, post_date):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    posts = user.posts.filter_by(date=post_date).all()
    if posts is None:
        return failure_response('Posts not found!')
    return success_response([p.serialize() for p in posts])

@app.route("/api/users/<int:user_id>/posts/", methods=["POST"])
def create_post(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    body = json.loads(request.data)
    date = body.get('date')
    location = body.get('location')
    pictures = body.get('pictures')
    entry = body.get('entry')
    if date is None:
        return failure_response("No date provided")
    if location is None:
        return failure_response("No location provided")
    if entry is None:
        return failure_response("No entry provided")
    new_post = Post(date=date, location=location, pictures=pictures, entry=entry, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize())


@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(user_id, post_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")

    post = user.posts.filter_by(id=post_id).first()
    if post is None:
        return failure_response('Post not found!')

    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route("/api/users/<int:user_id>/posts/<int:post_id>/", methods=["POST"])
def update_post(user_id, post_id):
    pass
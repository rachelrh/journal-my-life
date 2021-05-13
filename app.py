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


def get_user_by_username(username):
    return User.query.filter(User.username==username).first()


def get_user_by_session_token(session_token):
    return User.query.filter(User.session_token==session_token).first()


def get_user_by_update_token(update_token):
    return User.query.filter(User.update_token == update_token).first()


def extract_token(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, json.dumps({"error": "Missing auth header"})
    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        return False, json.dumps({"error": "Invalid auth header"})
    return True, bearer_token


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


# your routes here
@app.route("/api/register/", methods=["POST"])
def register_account():
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    if username is None or password is None:
        return json.dumps({"error": "Invalid email or password"})
    optional_user = get_user_by_username(username)
    if optional_user is not None:
        return json.dumps({"error": "User already exists"})
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return json.dumps(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    )


@app.route("/api/login/", methods=["POST"])
def login():
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    if username is None or password is None:
        return json.dumps({"error": "Invalid email or password"})
    user = get_user_by_username(username)
    success = user is not None and user.verify_password(password)
    if not success:
        return json.dumps({"error": "Incorrect username or password"})
    return json.dumps(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    )


@app.route("/session/", methods=["POST"])
def update_session():
    success, update_token = extract_token(request)
    if not success:
        return update_token
    user = get_user_by_update_token(update_token)
    if user is None:
        return json.dumps({"error": f"Invalid update token: {update_token}"})
    user.renew_session()
    db.session.commit()
    return json.dumps(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token,
        }
    )


@app.route("/api/login/posts/")
def get_all_posts():
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
    return success_response([p.serialize() for p in user.posts])


@app.route("/api/login/posts/<int:year>/<int:month>/<int:day>/")
def get_post_by_date(year, month, day):
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
    posts = user.posts
    sameDate = []
    for post in posts:
        if post.year == year and post.month == month and post.day == day:
            sameDate.append(post)
    if sameDate == []:
        return failure_response("No posts of this date")
    return success_response([p.serialize() for p in sameDate])


@app.route("/api/login/posts/", methods=["POST"])
def create_post():
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
    body = json.loads(request.data)
    year = body.get('year')
    month = body.get('month')
    day = body.get('day')
    location = body.get('location')
    entry = body.get('entry')
    if year is None or month is None or day is None:
        return failure_response("Invalid date provided")
    if location is None:
        return failure_response("No location provided")
    if entry is None:
        return failure_response("No entry provided")
    new_post = Post(year=year, month=month, day=day, location=location, entry=entry, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize())


@app.route("/api/login/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
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

@app.route("/api/login/posts/<int:post_id>/", methods=["POST"])
def update_post(post_id):
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")

    body = json.loads(request.data)
    post.location = body.get('location', post.location)
    post.entry = body.get('entry', post.entry)
    
    db.session.commit()
    return success_response(post.serialize())


@app.route("/api/login/posts/<int:post_id>/upload/", methods=['POST'])
def upload(post_id):
    success, session_token = extract_token(request)
    if not success: 
        return session_token
    user = get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({"error": "Invalid session token"})
        
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=True)


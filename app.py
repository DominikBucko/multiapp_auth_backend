from flask import Flask, request, abort
from hashlib import sha256
from models.usermodel import User
from models.appmodel import Application
import sessions
import jwt
import json
import os

JWT_PKEY = os.environ["JWT_PKEY"]

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login_attempt(email=None, password=None):
    if not email or not password:
        try:
            email = request.get_json()["email"]
            password = request.get_json()["password"]
        except KeyError:
            abort(400)

    password = sha256(password.encode('utf-8')).hexdigest()
    user = sessions.retrieve_user(email)

    if password == user.password:
        jwt_data = {
            "email": email
        }

        token = jwt.encode(jwt_data, JWT_PKEY)

        return json.dumps({"token": token})


@app.route("/register", methods=["POST"])
def register_attempt():
    email = None
    password = None

    try:
        email = request.get_json()["email"]
        password = request.get_json()["password"]
    except KeyError:
        abort(400)

    try:
        sessions.register(email, sha256(password.encode('utf-8')).hexdigest())
    except sessions.UserAlreadyExistsException:
        abort(409, "User already exists.")

    return login_attempt(email, password)


@app.route("/validate-token", methods=["POST"])
def validate_token():
    token = None
    authorization = None
    app_name = None

    try:
        authorization = request.headers["Authorization"]
        token = request.get_json()["token"]
    except KeyError:
        abort(400)

    try:
        app_name = jwt.decode(authorization, options={"verify_signature": False}, key=JWT_PKEY)["name"]
    except KeyError:
        abort(400)

    if sessions.retrieve_app(app_name):
        user_json = jwt.decode(token, options={"verify_signature": False}, key=JWT_PKEY)
        try:
            return json.dumps({"email": user_json["email"]})
        except KeyError:
            abort(400, "Invalid JWT content")

    abort(404)


@app.route("/app-register", methods=["POST"])
def register_app():
    name = None
    try:
        name = request.get_json()["name"]
    except KeyError:
        abort(400)

    try:
        sessions.register_app(name)
    except sessions.AppAlreadyExistsException:
        abort(409, "Conflict")

    jwt_content = {
        "name": name
    }

    return json.dumps({"token": jwt.encode(jwt_content, JWT_PKEY)})


app.run('0.0.0.0', 8088)

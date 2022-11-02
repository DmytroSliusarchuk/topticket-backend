from backend.app import app
from backend.models.user import User, UserSchema
from flask import jsonify
from marshmallow import ValidationError


@app.route("/")
def index():
    return "Hello world!"


@app.route("/api/v1/hello-world-<int:num>")
def hello_world(num):
    return f"<h1>Hello World {num}</h1>"

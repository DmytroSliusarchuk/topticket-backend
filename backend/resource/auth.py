from flask import jsonify, request
from marshmallow import ValidationError

from backend.app import app
from backend.models.user import User, UserSchema
from backend.app import bcrypt


@app.route("/user/register", methods=["POST"])
def register():
    user_data = request.get_json()

    schema = UserSchema()
    try:
        user = schema.load(user_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

    if User.find_by_username(user_data["username"]):
        return jsonify({'Error': f'User {user_data["username"]} already exists'}), 403

    if User.find_by_email(user_data["email"]):
        return jsonify({'Error': f'User with email {user_data["email"]} already exists'}), 403

    if User.find_by_phone(user_data["phone"]):
        return jsonify({'Error': f'User with phone {user_data["phone"]} already exists'}), 403

    user.password = bcrypt.generate_password_hash(password=user_data['password'])

    user.save_to_db()
    jwt_token = user.get_jwt()
    return jsonify({"access_token": jwt_token})


@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_username(data["username"])

    if not user:
        return jsonify({'message': f'User {data["username"]} doesn\'t exist'}), 404

    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({'message': 'Wrong password'}), 403

    access_token = user.get_jwt()

    return jsonify({'message': f'Logged in as {data["username"]}', 'access_token': access_token})

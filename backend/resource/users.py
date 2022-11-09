from backend.app import app
from backend.models.user import User, UserSchema
from flask import jsonify, request
from marshmallow import ValidationError, EXCLUDE
from backend.app import bcrypt
from flask_jwt_extended import jwt_required


@app.route('/user/<userid>', methods=['GET'])
@jwt_required()
def get_user_by_id(userid: int):
    user = User.query.get(userid)
    if not user:
        return jsonify({"Error": f"User with id={userid} not found"}), 404
    schema = UserSchema()
    result = schema.dump(user)
    return jsonify(result)


@app.route('/user/username/<username>', methods=['GET'])
@jwt_required()
def get_user_by_username(username: str):
    user = User.find_by_username(username)
    if not user:
        return jsonify({"Error": f"User with username={username} not found"}), 404
    schema = UserSchema()
    result = schema.dump(user)
    return jsonify(result)


@app.route('/user', methods=['PUT'])
@jwt_required()
def update_user_by_username():
    user_data = request.get_json()
    user_data["upd"] = 1
    if User.find_by_username(user_data["username"]):
        user_data['password'] = bcrypt.generate_password_hash(password=user_data['password'])

        schema = UserSchema()
        try:
            schema.load(user_data, unknown=EXCLUDE)
        except ValidationError as err:
            return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 400

        User.update_by_username(user_data)
        return jsonify({"Message": "User was updated"})
    else:
        return jsonify({"Error": f"User with username={user_data['username']} not found"}), 404


@app.route('/user/<userid>', methods=['DELETE'])
@jwt_required()
def delete_user_by_id(userid: int):
    return User.delete_by_id(userid)

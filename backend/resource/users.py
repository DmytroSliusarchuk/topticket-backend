from backend.app import app
from backend.models.user import User, UserSchema
from flask import jsonify, request
from marshmallow import ValidationError
from ..app import bcrypt


@app.route('/user/<username>', methods=['GET'])
def get_user_by_username(username: str):
    user = User.find_by_username(username)
    if not user:
        return jsonify({"Error": f"User with username={username} not found"}), 404
    schema = UserSchema()
    result = schema.dump(user)
    return jsonify(result)


@app.route('/user/<username>', methods=['PUT'])
def update_user_by_username(username: str):
    user_data = request.get_json()

    user_data['password'] = bcrypt.generate_password_hash(password=user_data['password'])

    schema = UserSchema()
    try:
        user = schema.load(user_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    try:
        user.update_by_username(username, user_data)
        return jsonify({"Message": "User was updated"})
    except:
        return jsonify({"Error": f"User with username={username} not found"}), 404


@app.route('/user/<username>', methods=['DELETE'])
def delete_user_by_username(username: str):
    try:
        User.delete_by_username(username)
        return jsonify({"Message": "User was deleted"})
    except:
        return jsonify({"Error": f"User with username={username} not found"}), 404

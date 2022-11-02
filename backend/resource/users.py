from backend.app import app
from backend.models.user import User, UserSchema
from flask import jsonify


@app.route('/user/<username>', methods=['GET'])
def get_user_by_username(username: str):
    user = User.find_by_username(username)
    if not user:
        return jsonify({"Error": f"User with username={username} not found"}), 404
    schema = UserSchema()
    result = schema.dump(user)
    return jsonify(result)

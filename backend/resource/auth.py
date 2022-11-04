from backend.app import app
from backend.models.user import User, UserSchema
from flask import jsonify, request
from marshmallow import ValidationError
from ..app import bcrypt


@app.route("/user/register", methods=["POST"])
def register():
    user_data = request.get_json()

    user_data['password'] = bcrypt.generate_password_hash(password=user_data['password'])

    schema = UserSchema()
    try:
        user = schema.load(user_data)
    except ValidationError as err:
        return jsonify({"Validation errors": [err.messages[mesg][0] for mesg in err.messages]}), 405

    if User.find_by_username(user_data["username"]):
        return jsonify({'Error': f'User {user_data["username"]} already exists'}), 403

    if User.find_by_email(user_data["email"]):
        return jsonify({'Error': f'User with email {user_data["email"]} already exists'}), 403

    if User.find_by_phone(user_data["phone"]):
        return jsonify({'Error': f'User with phone {user_data["phone"]} already exists'}), 403

    user.save_to_db()
    result = schema.dump(user)

    return jsonify(result)

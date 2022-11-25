from functools import wraps
from flask_jwt_extended import get_jwt_identity

from backend.models.user import User


def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        userid = get_jwt_identity()
        user = User.query.get(userid)
        if user.role == "Admin":
            return func(*args, **kwargs)
        return {'error': 'You do not have permission to access this resource!'}, 403

    return wrap

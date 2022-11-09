from backend.models.user import User
from functools import wraps

from flask_jwt_extended import get_jwt_identity


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        userid = get_jwt_identity()
        user = User.query.get(userid)
        if 'Admin' == user.role:
            return f(*args, **kwargs)
        return {'error': 'You do not have permission to access this resource!'}, 403

    return wrap
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app import mongo
from functools import wraps

def admin_require(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if mongo.db.users.find_one({'user': get_jwt_identity()['user']})['role'] == 'ADMIN_ROLE':
            return f(*args, **kwargs)
        else:
            return jsonify({'ok': False, 'message': 'Unauthorizaed user'}), 403

    return wrap
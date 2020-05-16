import os
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from app import app, mongo, flask_bcrypt, jwt
from app.schemas.user import validate_user
from functools import wraps
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'ok': False, 'message': 'Missing Authorization Header'}), 401

def admin_require(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if mongo.db.users.find_one({'user': get_jwt_identity()['user']})['role'] == 'ADMIN_ROLE':
            return f(*args, **kwargs)
        else:
            return jsonify({'ok': False, 'message': 'Unauthorizaed user'}), 401

    return wrap

@app.route('/auth', methods=['POST'])
def auth_user():
    try:
        data = validate_user(request.get_json())
        if not data['ok']:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

        data = data['data']
        user = mongo.db.users.find_one({'user': data['user']}, {'_id': False})
        if not user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            return jsonify({'ok': False, 'message': 'Invalid user or password'}), 401

        del user['password']
        del data['password']
        if not user['active']:
            return jsonify({'ok': False, 'message': 'Invalid user or password'}), 401

        access_token = create_access_token(identity=data)
        refresh_token = create_refresh_token(identity=data)
        user['token'] = access_token
        user['refresh'] = refresh_token
        return jsonify({'ok': True, 'data': user}), 200
    except:
        return jsonify({'ok': False, 'message': 'Invalid user or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = validate_user(request.get_json())
    if not data['ok']:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400

    data = data['data']
    data['password'] = flask_bcrypt.generate_password_hash(data['password'])
    data['role'] = 'USER_ROLE'
    data['active'] = False
    mongo.db.users.insert_one(data)
    return jsonify({'ok': True, 'message': 'User created successfully!'}), 201

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {'token': create_access_token(identity=current_user)}
    return jsonify({'ok': True, 'data': ret}), 200

@app.route('/user', methods=['GET'])
@jwt_required
@admin_require
def user():
    if request.method == 'GET':
        data = mongo.db.users.find({})
        users = []
        for user in data:
            users.append({'user': user['user'], 'role': user['role'], 'active': user['active']})
        return jsonify({'ok': True, 'data': users}), 200


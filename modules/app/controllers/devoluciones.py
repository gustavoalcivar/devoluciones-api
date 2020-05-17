import os
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app import app, mongo, jwt
from app.core.upload import upload_file
from app.core.read import exec_process
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({'ok': False, 'message': 'Missing Authorization Header'}), 401

@app.route('/devolucion', methods=['GET'])
@jwt_required
def devolucion():
    if request.method == 'GET':
        data = mongo.db.devoluciones.find({})
        devoluciones = []
        for devolucion in data:
            devoluciones.append({'ciudad': devolucion['ciudad'], 'local': devolucion['local'], 'anio': devolucion['anio'], 'mes': devolucion['mes'], 'dia': devolucion['dia'], 'bandejas': devolucion['bandejas']})
        return {'ok': True, 'data': devoluciones}, 200

@app.route('/upload', methods=['POST'])
@jwt_required
def upload():
    return upload_file(request)

@app.route('/read', methods=['GET'])
@jwt_required
def read():
    return exec_process()

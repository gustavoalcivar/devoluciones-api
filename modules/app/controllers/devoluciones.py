import os
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app import app, mongo, jwt
from app.core.upload import upload_file
from app.core.read import exec_process
from bson.son import SON
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
        tipo = request.args.get('tipo')
        if tipo == 'poranio':
            # Suma total de cada año
            pipeline = [
                {'$group': {'_id': '$anio', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('_id', 1)])}
            ]
        elif tipo == 'pormes':
            # Suma total de cada mes de un año
            try:
                anio = int(request.args.get('anio'))
            except:
                return {'ok': False, 'message': 'El año no es válido'}, 400
            if anio == None or anio == '':
                return {'ok': False, 'message': 'Debe ingresar el año en el parámetro -anio-'}, 400
            pipeline = [
                {'$match': {'anio': anio}},
                {'$group': {'_id': '$mes', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('_id', 1)])}
            ]
        elif tipo == 'pordia':
            # Suma total de cada día de un mes de un año
            try:
                anio = int(request.args.get('anio'))
                mes = int(request.args.get('mes'))
            except:
                return {'ok': False, 'message': 'El año o el mes no es válido'}, 400
            if anio == None or anio == '' or mes == None or mes == '':
                return {'ok': False, 'message': 'Debe ingresar el año en el parámetro -anio- y el mes en el parámetro -mes-'}, 400
            pipeline = [
                {'$match': {'anio': anio, 'mes': mes}},
                {'$group': {'_id': '$dia', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('_id', 1)])}
            ]
        elif tipo == 'porlocal':
            # Suma total de cada local de un día de un mes de un año
            try:
                anio = int(request.args.get('anio'))
                mes = int(request.args.get('mes'))
                dia = int(request.args.get('dia'))
            except:
                return {'ok': False, 'message': 'El año, el mes o el día no es válido'}, 400
            if anio == None or anio == '' or mes == None or mes == '' or dia == None or dia == '':
                return {'ok': False, 'message': 'Debe ingresar el año en el parámetro -anio- el mes en el parámetro -mes- y el día en el parámetro -dia-'}, 400
            pipeline = [
                {'$match': {'anio': anio, 'mes': mes, 'dia': dia}},
                {'$group': {'_id': '$local', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('dato', -1)])}
            ]
        elif tipo == 'porlocalenelmes':
            # Suma total agrupada por local de un mes de un año
            try:
                anio = int(request.args.get('anio'))
                mes = int(request.args.get('mes'))
            except:
                return {'ok': False, 'message': 'El año o el mes no es válido'}, 400
            if anio == None or anio == '' or mes == None or mes == '':
                return {'ok': False, 'message': 'Debe ingresar el año en el parámetro -anio- y el mes en el parámetro -mes-'}, 400
            pipeline = [
                {'$match': {'anio': anio, 'mes': mes}},
                {'$group': {'_id': '$local', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('dato', -1)])}
            ]
        elif tipo == 'deunlocalenelmes':
            # Suma total agrupada por dia de un local en un mes de un año
            try:
                local = request.args.get('local')
                mes = int(request.args.get('mes'))
                anio = int(request.args.get('anio'))
            except:
                return {'ok': False, 'message': 'El local, el mes o el año no es válido'}, 400
            if local == None or local == '' or mes == None or mes == '' or anio == None or anio == '':
                return {'ok': False, 'message': 'Debe ingresar el año en el parámetro -anio-, el mes en el parámetro -mes- y el local en el parametro -local-'}, 400
            pipeline = [
                {'$match': {'local': local, 'anio': anio, 'mes': mes}},
                {'$group': {'_id': '$dia', 'dato': {'$sum': '$bandejas'}}},
                {'$sort': SON([('_id', 1)])}
            ]
        else:
            return {'ok': False, 'message': 'Debe ingresar una opción válida en el parámetro -tipo-'}, 400
        data = mongo.db.devoluciones.aggregate(pipeline)
        devoluciones = []
        total = 0
        for devolucion in data:
            devoluciones.append({'etiqueta': devolucion['_id'], 'dato': devolucion['dato']})
            total = total + devolucion['dato']
        return {'ok': True, 'data': devoluciones, 'total': total}, 200

@app.route('/upload', methods=['POST'])
@jwt_required
def upload():
    return upload_file(request)

@app.route('/read', methods=['GET'])
@jwt_required
def read():
    return exec_process()

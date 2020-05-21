# dependencias instaladas con pip: flask, jsonschema, flask_bcrypt, flask_jwt_extended, flask_pymongo, dnspython, gunicorn, flask-cors
import os
import sys
from flask import jsonify, request

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import logger
from app import app

# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get('ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

try:
	PORT = os.environ['PORT'] # Lee las variables de entorno de Heroku
except:
	PORT = 4000

try:
    os.environ['FLASK_ENV'] = os.environ['FLASK_ENV']
except:
    os.environ['FLASK_ENV'] = 'development'

if os.environ['FLASK_ENV'] == 'development':
    app.config['DEBUG'] = True
    host = '0.0.0.0'
else:
    app.config['DEBUG'] = False
    host = os.environ['FLASK_HOST']

@app.errorhandler(404)
def not_found(error):
    LOG.error(error)
    return jsonify({'ok': False, 'message': str(error)}), 404

@app.route('/')
def index():
    return jsonify({'ok': True, 'message': 'Welcome!!!'})

if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('FLASK_ENV'))
    app.run(host=host, port=int(PORT)) # Run the app
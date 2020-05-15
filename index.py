# pip3 install flask
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
	PORT = 3000

try:
    os.environ['FLASK_ENV'] = os.environ['FLASK_ENV']
except:
    os.environ['FLASK_ENV'] = 'development'

if os.environ['FLASK_ENV'] == 'development':
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False

@app.errorhandler(404)
def not_found(error):
    LOG.error(error)
    return jsonify({'ok': False, 'message': str(error)}), 404

@app.route('/')
def index():
    return jsonify({'ok': True, 'message': 'Welcome!!!'})

if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('FLASK_ENV'))
    app.run(port=int(PORT)) # Run the app
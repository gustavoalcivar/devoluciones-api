import os
import json
import datetime
from flask import Flask
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

# create the flask object
app = Flask(__name__)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
try:
    os.environ['URL_DB'] = os.environ['URL_DB'] # Lee las variables de entorno de Heroku
except:
    os.environ['URL_DB'] = 'mongodb://localhost:27017/devoluciones'

app.config['MONGO_URI'] = os.environ.get('URL_DB')

try:
    os.environ['SECRET_KEY'] = os.environ['SECRET_KEY'] # Lee las variables de entorno de Heroku
except:
    os.environ['SECRET_KEY'] = 'clavesecretasolodedesarrollopilas'

app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=30)

mongo = PyMongo(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder

from app.controllers import *
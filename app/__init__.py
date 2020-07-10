from flask import abort, Flask, render_template, request, jsonify
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import os
import redis
import sys

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'gunicorn' in sys.argv[0] or '--heroku' in sys.argv or not sys.argv[0]: # Production database
  heroku = Heroku(app)
  r = redis.from_url(os.environ['REDIS_URL'])
else: # Development database
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nexus'
  r = redis.Redis(host='localhost', port=6379)
db = SQLAlchemy(app)

from . import routes as Routes

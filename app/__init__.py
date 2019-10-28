from flask import abort, Flask, render_template, request, jsonify
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if 'gunicorn' in sys.argv[0] or not sys.argv[0]: # Production database
  heroku = Heroku(app)
else: # Development database
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nexus'
db = SQLAlchemy(app)

from . import routes as Routes

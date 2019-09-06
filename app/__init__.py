from flask import abort, Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import sys

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if len(sys.argv) == 1: # development server
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nexus'
elif len(sys.argv) == 2: # production server
  heroku = Heroku(app)
db = SQLAlchemy(app)

from . import routes as Routes

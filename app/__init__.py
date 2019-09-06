from flask import abort, Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__, static_folder='static', static_url_path='')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/nexus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

from . import routes as Routes

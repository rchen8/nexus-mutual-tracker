# Import flask and template operators
from flask import abort, Flask, render_template, request, jsonify

# Define the WSGI application object
app = Flask(__name__, static_folder='static', static_url_path='')

from . import routes as Routes

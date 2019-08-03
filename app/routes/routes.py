from ..models import script
from flask import jsonify, render_template, request
from app import app

@app.route('/cover_amount_over_time', methods=['GET'])
def cover_amount_over_time():
  return jsonify(script.get_cover_amount_over_time())

@app.route('/cover_amount_per_contract', methods=['GET'])
def amount_per_contract():
  return jsonify(script.get_cover_amount_per_contract())

@app.route('/', methods=['GET'])
def index():
  script.get_etherscan_data()
  return render_template('index.html')

from ..models import script
from flask import jsonify, render_template, request
from app import app

@app.route('/active_cover_amount_over_time', methods=['GET'])
def active_cover_amount_over_time():
  return jsonify(script.get_active_cover_amount_over_time())

@app.route('/active_cover_amount_per_contract', methods=['GET'])
def active_cover_amount_per_contract():
  return jsonify(script.get_active_cover_amount_per_contract())

@app.route('/capital_pool_size_over_time', methods=['GET'])
def capital_pool_size_over_time():
  return jsonify(script.get_capital_pool_size_over_time())

@app.route('/', methods=['GET'])
def index():
  script.get_etherscan_data()
  return render_template('index.html')

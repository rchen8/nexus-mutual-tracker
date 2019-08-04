from ..models import script
from flask import jsonify, render_template, request
from app import app

@app.route('/active_cover_amount', methods=['GET'])
def active_cover_amount():
  return jsonify(script.get_active_cover_amount())

@app.route('/active_cover_amount_per_contract', methods=['GET'])
def active_cover_amount_per_contract():
  return jsonify(script.get_active_cover_amount_per_contract())

@app.route('/capital_pool_size', methods=['GET'])
def capital_pool_size():
  return jsonify(script.get_capital_pool_size())

@app.route('/capital_pool_distribution', methods=['GET'])
def capital_pool_distribution():
  return jsonify(script.get_capital_pool_distribution())

@app.route('/mcr_percentage', methods=['GET'])
def mcr_percentage():
  return jsonify(script.get_mcr_percentage())

@app.route('/nxm_token_price', methods=['GET'])
def nxm_token_price():
  return jsonify(script.get_nxm_token_price())

@app.route('/', methods=['GET'])
def index():
  script.get_etherscan_data()
  return render_template('index.html')

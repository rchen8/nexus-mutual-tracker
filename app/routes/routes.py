from ..models import parser, script
from flask import jsonify, render_template, request
from app import app

@app.route('/', methods=['GET'])
def index():
  parser.parse_etherscan_data()
  return render_template('covers.html')

@app.route('/covers', methods=['GET'])
def covers():
  return jsonify(script.get_covers())

@app.route('/active_cover_amount', methods=['GET'])
def active_cover_amount():
  return jsonify(script.get_active_cover_amount())

@app.route('/active_cover_amount_per_contract', methods=['GET'])
def active_cover_amount_per_contract():
  return jsonify(script.get_active_cover_amount_per_contract())

####################################################################################################

@app.route('/capital_pool', methods=['GET'])
def capital_pool():
  parser.parse_etherscan_data()
  return render_template('capital_pool.html')

@app.route('/capital_pool_size', methods=['GET'])
def capital_pool_size():
  return jsonify(script.get_capital_pool_size())

@app.route('/capital_pool_distribution', methods=['GET'])
def capital_pool_distribution():
  return jsonify(script.get_capital_pool_distribution())

@app.route('/mcr_percentage', methods=['GET'])
def mcr_percentage():
  return jsonify(script.get_mcr_percentage())

####################################################################################################

@app.route('/staked', methods=['GET'])
def staked():
  parser.parse_etherscan_data()
  return render_template('staked.html')

@app.route('/total_amount_staked', methods=['GET'])
def total_amount_staked():
  return jsonify(script.get_total_amount_staked())

@app.route('/amount_staked_per_contract', methods=['GET'])
def amount_staked_per_contract():
  return jsonify(script.get_amount_staked_per_contract())

####################################################################################################

@app.route('/token', methods=['GET'])
def token():
  parser.parse_etherscan_data()
  return render_template('token.html')

@app.route('/nxm_token_price', methods=['GET'])
def nxm_token_price():
  return jsonify(script.get_nxm_token_price())

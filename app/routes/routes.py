from ..models import parser, script
from flask import jsonify, render_template, request, send_from_directory
from app import app
import os

@app.route('/active_cover_amount', methods=['GET'])
def active_cover_amount():
  return jsonify(script.get_active_cover_amount())

@app.route('/active_cover_amount_per_contract', methods=['GET'])
def active_cover_amount_per_contract():
  return jsonify(script.get_active_cover_amount_per_contract())

@app.route('/all_covers', methods=['GET'])
def all_covers():
  return jsonify(script.get_all_covers())

@app.route('/capital_pool_size', methods=['GET'])
def capital_pool_size():
  return jsonify(script.get_capital_pool_size())

@app.route('/mcr_percentage', methods=['GET'])
def mcr_percentage():
  return jsonify(script.get_mcr_percentage(over_100=True))

@app.route('/total_amount_staked', methods=['GET'])
def total_amount_staked():
  return jsonify(script.get_total_amount_staked())

@app.route('/all_stakes', methods=['GET'])
def all_stakes():
  return jsonify(script.get_all_stakes())

@app.route('/amount_staked_per_contract', methods=['GET'])
def amount_staked_per_contract():
  return jsonify(script.get_amount_staked_per_contract())

@app.route('/nxm_price', methods=['GET'])
def nxm_price():
  return jsonify(script.get_nxm_price())

@app.route('/nxm_supply', methods=['GET'])
def nxm_supply():
  return jsonify(script.get_nxm_supply())

@app.route('/nxm_market_cap', methods=['GET'])
def nxm_market_cap():
  return jsonify(script.get_nxm_market_cap())

@app.route('/nxm_distribution', methods=['GET'])
def nxm_distribution():
  return jsonify(script.get_nxm_distribution())

####################################################################################################

@app.route('/<template>', methods=['GET'])
def render(template):
  parser.parse_etherscan_data()
  return render_template(template + '.html')

@app.route('/', methods=['GET'])
def index():
  parser.parse_etherscan_data()
  return render_template('covers.html')

@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.gif',
      mimetype='image/vnd.microsoft.icon')

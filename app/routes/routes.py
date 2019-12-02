from ..models import parser, script
from flask import jsonify, render_template, request, send_from_directory
from app import app
import os

@app.route('/active_cover_amount', methods=['GET'])
def active_cover_amount():
  return jsonify(script.get_active_cover_amount(cache=True))

@app.route('/active_cover_amount_per_contract', methods=['GET'])
def active_cover_amount_per_contract():
  return jsonify(script.get_active_cover_amount_per_contract(cache=True))

@app.route('/active_cover_amount_by_expiration_date', methods=['GET'])
def active_cover_amount_by_expiration_date():
  return jsonify(script.get_active_cover_amount_by_expiration_date(cache=True))

@app.route('/all_covers', methods=['GET'])
def all_covers():
  return jsonify(script.get_all_covers(cache=True))

@app.route('/capital_pool_size', methods=['GET'])
def capital_pool_size():
  return jsonify(script.get_capital_pool_size(cache=True))

@app.route('/minimum_capital_requirement', methods=['GET'])
def minimum_capital_requirement():
  return jsonify(script.get_minimum_capital_requirement(cache=True))

@app.route('/mcr_percentage', methods=['GET'])
def mcr_percentage():
  return jsonify(script.get_mcr_percentage(over_100=True, cache=True))

@app.route('/total_amount_staked', methods=['GET'])
def total_amount_staked():
  return jsonify(script.get_total_amount_staked(cache=True))

@app.route('/amount_staked_per_contract', methods=['GET'])
def amount_staked_per_contract():
  return jsonify(script.get_amount_staked_per_contract(cache=True))

@app.route('/total_staking_reward', methods=['GET'])
def total_staking_reward():
  return jsonify(script.get_total_staking_reward(cache=True))

@app.route('/staking_reward_per_contract', methods=['GET'])
def staking_reward_per_contract():
  return jsonify(script.get_staking_reward_per_contract(cache=True))

@app.route('/all_stakes', methods=['GET'])
def all_stakes():
  return jsonify(script.get_all_stakes(cache=True))

@app.route('/nxm_price', methods=['GET'])
def nxm_price():
  return jsonify(script.get_nxm_price(cache=True))

@app.route('/nxm_supply', methods=['GET'])
def nxm_supply():
  return jsonify(script.get_nxm_supply(cache=True))

@app.route('/nxm_market_cap', methods=['GET'])
def nxm_market_cap():
  return jsonify(script.get_nxm_market_cap(cache=True))

@app.route('/nxm_distribution', methods=['GET'])
def nxm_distribution():
  return jsonify(script.get_nxm_distribution(cache=True))

####################################################################################################

@app.route('/<template>', methods=['GET'])
def render(template):
  return render_template(template + '.html')

@app.route('/', methods=['GET'])
def index():
  return render_template('covers.html')

@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.gif',
      mimetype='image/vnd.microsoft.icon')

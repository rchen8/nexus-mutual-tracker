from ..models import parser, grapher, utils
from flask import jsonify, make_response, redirect, render_template, send_from_directory
from app import app
import csv
import io
import os

@app.route('/active_cover_amount', methods=['GET'])
def active_cover_amount():
  return jsonify(grapher.get_active_cover_amount(cache=True))

@app.route('/active_cover_amount_per_project', methods=['GET'])
def active_cover_amount_per_project():
  return jsonify(grapher.get_active_cover_amount_per_project(cache=True))

@app.route('/active_cover_amount_by_expiration_date', methods=['GET'])
def active_cover_amount_by_expiration_date():
  return jsonify(grapher.get_active_cover_amount_by_expiration_date(cache=True))

@app.route('/defi_tvl_covered', methods=['GET'])
def defi_tvl_covered():
  return jsonify(grapher.get_defi_tvl_covered(cache=True))

@app.route('/annualized_premiums_in_force', methods=['GET'])
def annualized_premiums_in_force():
  return jsonify(grapher.get_annualized_premiums_in_force(cache=True))

@app.route('/total_premiums_paid', methods=['GET'])
def total_premiums_paid():
  return jsonify(grapher.get_total_premiums_paid(cache=True))

@app.route('/premiums_paid_per_project', methods=['GET'])
def premiums_paid_per_project():
  return jsonify(grapher.get_premiums_paid_per_project(cache=True))

@app.route('/monthly_surplus', methods=['GET'])
def monthly_surplus():
  return jsonify(grapher.get_monthly_surplus(cache=True))

@app.route('/all_covers', methods=['GET'])
def all_covers():
  return jsonify(grapher.get_all_covers(cache=True))

@app.route('/all_claims', methods=['GET'])
def all_claims():
  return jsonify(grapher.get_all_claims(cache=True))

@app.route('/all_votes', methods=['GET'])
def all_votes():
  return jsonify(grapher.get_all_votes(cache=True))

@app.route('/capital_pool_size', methods=['GET'])
def capital_pool_size():
  return jsonify(grapher.get_capital_pool_size(cache=True))

@app.route('/capital_efficiency_ratio', methods=['GET'])
def capital_efficiency_ratio():
  return jsonify(grapher.get_capital_efficiency_ratio(cache=True))

@app.route('/minimum_capital_requirement', methods=['GET'])
def minimum_capital_requirement():
  return jsonify(grapher.get_minimum_capital_requirement(cache=True))

@app.route('/current_mcr_percentage', methods=['GET'])
def current_mcr_percentage():
  return jsonify(utils.get_current_mcr_percentage())

@app.route('/mcr_percentage', methods=['GET'])
def mcr_percentage():
  return jsonify(grapher.get_mcr_percentage(cache=True))

@app.route('/total_amount_staked', methods=['GET'])
def total_amount_staked():
  return jsonify(grapher.get_total_amount_staked(cache=True))

@app.route('/amount_staked_per_project', methods=['GET'])
def amount_staked_per_project():
  return jsonify(grapher.get_amount_staked_per_project(cache=True))

@app.route('/top_stakers', methods=['GET'])
def top_stakers():
  return jsonify(grapher.get_top_stakers(cache=True))

@app.route('/total_staking_reward', methods=['GET'])
def total_staking_reward():
  return jsonify(grapher.get_total_staking_reward(cache=True))

@app.route('/staking_reward_per_project', methods=['GET'])
def staking_reward_per_project():
  return jsonify(grapher.get_staking_reward_per_project(cache=True))

@app.route('/nxm_price', methods=['GET'])
def nxm_price():
  return jsonify(grapher.get_nxm_price(cache=True))

@app.route('/nxm_daily_volume', methods=['GET'])
def nxm_daily_volume():
  return jsonify(grapher.get_nxm_daily_volume(cache=True))

@app.route('/nxm_supply', methods=['GET'])
def nxm_supply():
  return jsonify(grapher.get_nxm_supply(cache=True))

@app.route('/nxm_market_cap', methods=['GET'])
def nxm_market_cap():
  return jsonify(grapher.get_nxm_market_cap(cache=True))

@app.route('/net_market_cap', methods=['GET'])
def net_market_cap():
  return jsonify(grapher.get_net_market_cap(cache=True))

@app.route('/book_value_ratio', methods=['GET'])
def book_value_ratio():
  return jsonify(grapher.get_book_value_ratio(cache=True))

@app.route('/nxm_distribution', methods=['GET'])
def nxm_distribution():
  return jsonify(grapher.get_nxm_distribution(cache=True))

@app.route('/unique_addresses', methods=['GET'])
def unique_addresses():
  return jsonify(grapher.get_unique_addresses(cache=True))

####################################################################################################

@app.route('/download/<graph>', methods=['GET'])
def download(graph):
  si = io.StringIO()
  writer = csv.writer(si)
  writer.writerows(utils.json_to_csv(graph))
  output = make_response(si.getvalue())
  output.headers['Content-Disposition'] = 'attachment; filename=%s.csv' % graph
  output.headers['Content-type'] = 'text/csv'
  return output

@app.route('/token', methods=['GET'])
def token():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('token.html')

@app.route('/staking', methods=['GET'])
def staking():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('staking.html')

@app.route('/capital_pool', methods=['GET'])
def capital_pool():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('capital_pool.html')

@app.route('/claims', methods=['GET'])
def claims():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('claims.html')

@app.route('/covers', methods=['GET'])
def covers():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('covers.html')

@app.route('/', methods=['GET'])
def index():
  return redirect('https://dune.com/rchen8/nexus-mutual', code=302)
  # return render_template('covers.html')

@app.route('/favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.gif',
      mimetype='image/vnd.microsoft.icon')

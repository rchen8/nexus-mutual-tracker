from .models import *
from .utils import *
from collections import defaultdict
from datetime import datetime, timedelta
from intervaltree import IntervalTree
import bisect
import json
import os
import redis
import sys

if 'gunicorn' in sys.argv[0] or 'job.py' in sys.argv[0] or not sys.argv[0]: # Production Redis
  r = redis.from_url(os.environ['REDIS_URL'])
else: # Development Redis
  r = redis.Redis(host='localhost', port=6379)

def get_active_cover_amount(cache=False):
  if cache:
    return json.loads(r.get('cover_amount'))

  times = []
  tree = IntervalTree()
  for cover in query_table(Cover):
    times.append(cover['start_time'])
    times.append(cover['end_time'])
    tree[cover['start_time']:cover['end_time']] = (cover['amount'], cover['currency'])

  cover_amount = {'USD': {}, 'ETH': {}}
  for time in times:
    if time < datetime.now():
      intervals = tree[time]
      eth_price = get_historical_crypto_price('ETH', time)
      dai_price = get_historical_crypto_price('DAI', time)

      cover_amount['USD'][time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data[0] * (eth_price if interval.data[1] == 'ETH' else dai_price) \
              for interval in intervals])
      cover_amount['ETH'][time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data[0] / (1 if interval.data[1] == 'ETH' else eth_price / dai_price) \
              for interval in intervals])
  return cover_amount

def get_active_cover_amount_per_contract(cache=False):
  if cache:
    return json.loads(r.get('cover_amount_per_contract'))
  if not price:
    set_current_crypto_prices()

  cover_amount_per_contract = {'USD': defaultdict(int), 'ETH': defaultdict(int)}
  for cover in query_table(Cover):
    if datetime.now() < cover['end_time']:
      cover_amount_per_contract['USD'][cover['contract_name']] += \
          cover['amount'] * price[cover['currency']]
      cover_amount_per_contract['ETH'][cover['contract_name']] += \
          cover['amount'] / (1 if cover['currency'] == 'ETH' else price['ETH'] / price['DAI'])
  return dict(cover_amount_per_contract)

def get_active_cover_amount_by_expiration_date(cache=False):
  if cache:
    return json.loads(r.get('cover_amount_by_expiration_date'))
  if not price:
    set_current_crypto_prices()

  cover_amount_by_expiration_date = {'USD': defaultdict(int), 'ETH': defaultdict(int)}
  covers = query_table(Cover)

  last_cover_amount_usd = 0
  last_cover_amount_eth = 0
  for cover in covers:
    if datetime.now() < cover['end_time']:
      last_cover_amount_usd += cover['amount'] * price[cover['currency']]
      last_cover_amount_eth += \
          cover['amount'] / (1 if cover['currency'] == 'ETH' else price['ETH'] / price['DAI'])

  covers.sort(key=lambda x: x['end_time'])
  for cover in covers:
    if datetime.now() < cover['end_time']:
      end_time = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
      last_cover_amount_usd -= cover['amount'] * price[cover['currency']]
      last_cover_amount_eth -= \
          cover['amount'] / (1 if cover['currency'] == 'ETH' else price['ETH'] / price['DAI'])
      cover_amount_by_expiration_date['USD'][end_time] = last_cover_amount_usd
      cover_amount_by_expiration_date['ETH'][end_time] = last_cover_amount_eth
  return dict(cover_amount_by_expiration_date)

def get_all_covers(cache=False):
  if cache:
    return json.loads(r.get('covers'))
  if not price:
    set_current_crypto_prices()

  covers = query_table(Cover)
  for cover in covers:
    cover['start_time'] = cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['end_time'] = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['amount_usd'] = cover['amount'] * price[cover['currency']]
    cover['premium_usd'] = cover['premium'] * price[cover['currency']]
  return covers

def get_capital_pool_size(cache=False):
  if cache:
    return json.loads(r.get('capital_pool_size'))

  txns = query_table(Transaction)
  txns.sort(key=lambda x: x['timestamp'])
  total = defaultdict(int)
  capital_pool_size = {'USD': {}, 'ETH': {}}
  for txn in txns:
    total[txn['currency']] += txn['amount']
    eth_price = get_historical_crypto_price('ETH', txn['timestamp'])
    dai_price = get_historical_crypto_price('DAI', txn['timestamp'])

    capital_pool_size['USD'][txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total['ETH'] * eth_price + total['DAI'] * dai_price
    capital_pool_size['ETH'][txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total['ETH'] + total['DAI'] / (eth_price / dai_price)
  return capital_pool_size

def get_minimum_capital_requirement(cache=False):
  if cache:
    return json.loads(r.get('minimum_capital_requirement'))

  minimum_capital_requirement = {}
  minimum_capital_requirement['2019-07-12 08:44:52'] = 7000
  minimum_capital_requirement['2019-11-06 07:00:03'] = 7000
  for txn in query_table(MinimumCapitalRequirement):
    minimum_capital_requirement[txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = txn['mcr']
  return minimum_capital_requirement

def get_mcr_percentage(over_100, cache=False):
  if over_100 and cache:
    return json.loads(r.get('mcr_percentage'))

  capital_pool_size = get_capital_pool_size()
  mcrs = query_table(MinimumCapitalRequirement, order=MinimumCapitalRequirement.timestamp)
  mcr_percentage = {}
  for time in capital_pool_size['ETH']:
    if over_100 and capital_pool_size['ETH'][time] < timestamp_to_mcr(mcrs, time):
      continue
    mcr_percentage[time] = capital_pool_size['ETH'][time] / timestamp_to_mcr(mcrs, time) * 100
  return mcr_percentage

def get_nxm_price(cache=False):
  if cache:
    return json.loads(r.get('nxm_price'))

  A = 1028 / 10**5
  C = 5800000
  mcrs = query_table(MinimumCapitalRequirement, order=MinimumCapitalRequirement.timestamp)
  mcr_percentage = get_mcr_percentage(over_100=False)
  nxm_price = {'USD': {}, 'ETH': {}}
  for time in mcr_percentage:
    eth_price = get_historical_crypto_price('ETH', datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    nxm_price['USD'][time] = \
        (A + (timestamp_to_mcr(mcrs, time) / C) * (mcr_percentage[time] / 100)**4) * eth_price
    nxm_price['ETH'][time] = \
        A + (timestamp_to_mcr(mcrs, time) / C) * (mcr_percentage[time] / 100)**4
  price['NXM'] = nxm_price['USD'][max(nxm_price['USD'])]
  return nxm_price

def get_total_amount_staked(cache=False):
  if cache:
    return json.loads(r.get('amount_staked'))

  nxm_price = get_nxm_price()
  times = []
  tree = IntervalTree()
  for txn in query_table(StakingTransaction):
    times.append(txn['start_time'])
    times.append(txn['end_time'])
    tree[txn['start_time']:txn['end_time']] = txn['amount']

  amount_staked = {'USD': {}, 'NXM': {}}
  nxm_times = sorted(nxm_price['USD'].keys())
  for time in times:
    if time < datetime.now():
      intervals = tree[time]
      historical_nxm_price = nxm_price['USD'] \
          [nxm_times[bisect.bisect(nxm_times, time.strftime('%Y-%m-%d %H:%M:%S')) - 1]]

      amount_staked['USD'][time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data for interval in intervals]) * historical_nxm_price
      amount_staked['NXM'][time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data for interval in intervals])
  return amount_staked

def get_amount_staked_per_contract(cache=False):
  if cache:
    return json.loads(r.get('amount_staked_per_contract'))

  get_nxm_price()
  amount_staked_per_contract = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for txn in query_table(StakingTransaction):
    if datetime.now() < txn['end_time']:
      amount_staked_per_contract['USD'][txn['contract_name']] += txn['amount'] * price['NXM']
      amount_staked_per_contract['NXM'][txn['contract_name']] += txn['amount']
  return dict(amount_staked_per_contract)

def get_total_staking_reward(cache=False):
  if cache:
    return json.loads(r.get('staking_reward'))

  nxm_price = get_nxm_price()
  nxm_times = sorted(nxm_price['USD'].keys())
  total = 0
  staking_reward = {'USD': {}, 'NXM': {}}
  for reward in query_table(StakingReward, order=StakingReward.timestamp):
    total += reward['amount']
    historical_nxm_price = nxm_price['USD'] \
        [nxm_times[bisect.bisect(nxm_times, reward['timestamp'].strftime('%Y-%m-%d %H:%M:%S')) - 1]]

    staking_reward['USD'][reward['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total * historical_nxm_price
    staking_reward['NXM'][reward['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = total
  return staking_reward

def get_staking_reward_per_contract(cache=False):
  if cache:
    return json.loads(r.get('staking_reward_per_contract'))

  get_nxm_price()
  staking_reward_per_contract = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for reward in query_table(StakingReward):
    staking_reward_per_contract['USD'][reward['contract_name']] += reward['amount'] * price['NXM']
    staking_reward_per_contract['NXM'][reward['contract_name']] += reward['amount']
  return dict(staking_reward_per_contract)

def get_all_stakes(cache=False):
  if cache:
    return json.loads(r.get('stakes'))

  get_nxm_price()
  stakes = query_table(StakingTransaction)
  for stake in stakes:
    stake['start_time'] = stake['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    stake['end_time'] = stake['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    stake['amount_usd'] = stake['amount'] * price['NXM']
  return stakes

def get_nxm_supply(cache=False):
  if cache:
    return json.loads(r.get('nxm_supply'))

  bonding_curve_address = '0x0000000000000000000000000000000000000000'
  txns = query_table(NXMTransaction)
  txns.sort(key=lambda x: x['timestamp'])
  total = 0
  nxm_supply = {}
  for txn in txns:
    if txn['from_address'] == bonding_curve_address:
      total += txn['amount']
      if total > 0:
        nxm_supply[txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = total
    elif txn['to_address'] == bonding_curve_address:
      total -= txn['amount']
      if total > 0:
        nxm_supply[txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = total
  return nxm_supply

def get_nxm_market_cap(cache=False):
  if cache:
    return json.loads(r.get('nxm_market_cap'))

  nxm_price = get_nxm_price()
  nxm_supply = get_nxm_supply()
  nxm_times = sorted(nxm_price['USD'].keys())
  nxm_market_cap = {'USD': {}, 'ETH': {}}
  for time in nxm_supply:
    timestamp = nxm_times[bisect.bisect(nxm_times, time) - 1]
    nxm_price_usd = nxm_price['USD'][timestamp]
    nxm_price_eth = nxm_price['ETH'][timestamp]
    nxm_market_cap['USD'][time] = nxm_price_usd * nxm_supply[time]
    nxm_market_cap['ETH'][time] = nxm_price_eth * nxm_supply[time]
  return nxm_market_cap

def get_nxm_distribution(cache=False):
  if cache:
    return json.loads(r.get('nxm_distribution'))

  nxm_distribution = defaultdict(int)
  for txn in query_table(NXMTransaction):
    nxm_distribution[txn['from_address']] -= txn['amount']
    nxm_distribution[txn['to_address']] += txn['amount']

  for address in list(nxm_distribution):
    if nxm_distribution[address] < 10**-8:
      del nxm_distribution[address]
  nxm_distribution['Staking Contract'] = \
      nxm_distribution.pop('0x5407381b6c251cfd498ccd4a1d877739cb7960b8')
  return nxm_distribution

def cache_graph_data():
  r.set('cover_amount', json.dumps(get_active_cover_amount(cache=False)))
  r.set('cover_amount_per_contract', json.dumps(get_active_cover_amount_per_contract(cache=False)))
  r.set('cover_amount_by_expiration_date',
      json.dumps(get_active_cover_amount_by_expiration_date(cache=False)))
  r.set('covers', json.dumps(get_all_covers(cache=False)))
  r.set('capital_pool_size', json.dumps(get_capital_pool_size(cache=False)))
  r.set('minimum_capital_requirement', json.dumps(get_minimum_capital_requirement(cache=False)))
  r.set('mcr_percentage', json.dumps(get_mcr_percentage(over_100=True, cache=False)))
  r.set('nxm_price', json.dumps(get_nxm_price(cache=False)))
  r.set('amount_staked', json.dumps(get_total_amount_staked(cache=False)))
  r.set('amount_staked_per_contract', json.dumps(get_amount_staked_per_contract(cache=False)))
  r.set('staking_reward', json.dumps(get_total_staking_reward(cache=False)))
  r.set('staking_reward_per_contract', json.dumps(get_staking_reward_per_contract(cache=False)))
  r.set('stakes', json.dumps(get_all_stakes(cache=False)))
  r.set('nxm_supply', json.dumps(get_nxm_supply(cache=False)))
  r.set('nxm_market_cap', json.dumps(get_nxm_market_cap(cache=False)))
  r.set('nxm_distribution', json.dumps(get_nxm_distribution(cache=False)))

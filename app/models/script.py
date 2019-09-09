from .models import Cover, Transaction, StakingTransaction
from .utils import get_historical_crypto_price, price, query_table
from collections import defaultdict
from datetime import datetime, timedelta
from intervaltree import IntervalTree
import bisect

MINIMUM_CAPITAL_REQUIREMENT = 7000

capital_pool_size = {}
mcr_percentage = {}
nxm_price = {}

def get_active_cover_amount():
  times = []
  tree = IntervalTree()
  for cover in query_table(Cover):
    times.append(cover['start_time'])
    times.append(cover['end_time'])
    tree[cover['start_time']:cover['end_time']] = (cover['amount'], cover['currency'])

  cover_amount = {}
  for time in times:
    if time < datetime.now():
      intervals = tree[time]
      cover_amount[time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data[0] * get_historical_crypto_price(interval.data[1], time) \
              for interval in intervals])
  return cover_amount

def get_active_cover_amount_per_contract():
  cover_amount_per_contract = defaultdict(int)
  for cover in query_table(Cover):
    if datetime.now() < cover['end_time']:
      cover_amount_per_contract[cover['contract_name']] += \
          cover['amount'] * price[cover['currency']]
  return dict(cover_amount_per_contract)

def get_all_covers():
  covers = query_table(Cover)
  for cover in covers:
    cover['start_time'] = cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['end_time'] = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['amount'] = cover['amount'] * price[cover['currency']]
  return covers

def get_capital_pool_size():
  if capital_pool_size:
    return capital_pool_size

  txns = query_table(Transaction)
  txns.sort(key=lambda x: x['timestamp'])
  total = defaultdict(int)
  for txn in txns:
    total[txn['currency']] += txn['amount']
    capital_pool_size[txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total['ETH'] * get_historical_crypto_price('ETH', txn['timestamp']) + \
        total['DAI'] * get_historical_crypto_price('DAI', txn['timestamp'])
  return capital_pool_size

def get_capital_pool_distribution():
  nxm_address = '0xfd61352232157815cf7b71045557192bf0ce1884'
  capital_pool_distribution = defaultdict(int)
  for txn in query_table(Transaction):
    if txn['from_address'] != nxm_address:
      capital_pool_distribution[txn['from_address']] += txn['amount'] * price[txn['currency']]
    elif txn['to_address'] != nxm_address:
      capital_pool_distribution[txn['to_address']] -= txn['amount'] * price[txn['currency']]
  return capital_pool_distribution

def get_mcr_percentage():
  if mcr_percentage:
    return mcr_percentage

  get_capital_pool_size()
  for time in capital_pool_size:
    eth_price = get_historical_crypto_price('ETH', datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    if capital_pool_size[time] / eth_price > MINIMUM_CAPITAL_REQUIREMENT:
      mcr_percentage[time] = \
          (capital_pool_size[time] / eth_price) / MINIMUM_CAPITAL_REQUIREMENT * 100
  return mcr_percentage

def get_nxm_token_price():
  if nxm_price:
    return nxm_price

  A = 1028 / 10**5
  C = 5800000
  get_mcr_percentage()
  for time in mcr_percentage:
    eth_price = get_historical_crypto_price('ETH', datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    nxm_price[time] = \
        (A + (MINIMUM_CAPITAL_REQUIREMENT / C) * (mcr_percentage[time] / 100)**4) * eth_price
  price['NXM'] = nxm_price[max(nxm_price)]
  return nxm_price

def get_total_amount_staked():
  if not nxm_price:
    get_nxm_token_price()

  times = []
  tree = IntervalTree()
  for txn in query_table(StakingTransaction):
    times.append(txn['start_time'])
    times.append(txn['end_time'])
    tree[txn['start_time']:txn['end_time']] = txn['amount']

  amount_staked = {}
  nxm_times = sorted(nxm_price.keys())
  for time in times:
    if time < datetime.now():
      intervals = tree[time]
      amount_staked[time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data for interval in intervals]) * \
          nxm_price[nxm_times[bisect.bisect(nxm_times, time.strftime('%Y-%m-%d %H:%M:%S')) - 1]]
  return amount_staked

def get_amount_staked_per_contract():
  if not nxm_price:
    get_nxm_token_price()

  amount_staked_per_contract = defaultdict(int)
  for txn in query_table(StakingTransaction):
    if datetime.now() < txn['end_time']:
      amount_staked_per_contract[txn['contract_name']] += txn['amount'] * price['NXM']
  return dict(amount_staked_per_contract)

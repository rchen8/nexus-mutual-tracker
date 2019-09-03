from .utils import price, query_table
from collections import defaultdict
from datetime import datetime, timedelta
from intervaltree import IntervalTree

MINIMUM_CAPITAL_REQUIREMENT = 7000

capital_pool_size_over_time = {}
mcr_percentage_over_time = {}
nxm_price_over_time = {}

def get_active_cover_amount():
  times = []
  tree = IntervalTree()
  covers = query_table('Covers')
  for cover in covers:
    times.append(cover['start_time'])
    times.append(cover['end_time'])
    tree[cover['start_time']:cover['end_time']] = cover['amount']

  amount_over_time = {}
  for time in times:
    if datetime.now() > datetime.strptime(time, '%Y-%m-%d %H:%M:%S'):
      intervals = tree[time]
      amount_over_time[time] = sum([interval.data for interval in intervals])
  return amount_over_time

def get_active_cover_amount_per_contract():
  amount_per_contract = defaultdict(int)
  covers = query_table('Covers')
  for cover in covers:
    if datetime.now() < datetime.strptime(cover['end_time'], '%Y-%m-%d %H:%M:%S'):
      amount_per_contract[cover['contract_name']] += cover['amount']
  return dict(amount_per_contract)

def get_covers():
  return query_table('Covers')

def get_capital_pool_size():
  if capital_pool_size_over_time:
    return capital_pool_size_over_time

  transactions = query_table('Transactions')
  transactions.sort(key=lambda x: x['_timestamp'])
  total = 0
  for txn in transactions:
    total += txn['amount']
    capital_pool_size_over_time[txn['_timestamp']] = total
  return capital_pool_size_over_time

def get_capital_pool_distribution():
  nxm_address = '0xfd61352232157815cf7b71045557192bf0ce1884'
  capital_pool_distribution = defaultdict(int)
  transactions = query_table('Transactions')
  for txn in transactions:
    if txn['from_address'] != nxm_address:
      capital_pool_distribution[txn['from_address']] += txn['amount']
    elif txn['to_address'] != nxm_address:
      capital_pool_distribution[txn['to_address']] -= txn['amount']
  return capital_pool_distribution

def get_mcr_percentage():
  if mcr_percentage_over_time:
    return mcr_percentage_over_time

  get_capital_pool_size()
  for time in capital_pool_size_over_time:
    if capital_pool_size_over_time[time] / price['ETH'] > MINIMUM_CAPITAL_REQUIREMENT:
      mcr_percentage_over_time[time] = (capital_pool_size_over_time[time] / price['ETH']) / \
          MINIMUM_CAPITAL_REQUIREMENT * 100
  return mcr_percentage_over_time

def get_nxm_token_price():
  if nxm_price_over_time:
    return nxm_price_over_time

  A = 1028 / 10**5
  C = 5800000
  get_mcr_percentage()
  for time in mcr_percentage_over_time:
    nxm_price_over_time[time] = \
        (A + (MINIMUM_CAPITAL_REQUIREMENT / C) * (mcr_percentage_over_time[time] / 100)**4) * \
        price['ETH']
  price['NXM'] = nxm_price_over_time[max(nxm_price_over_time)]
  return nxm_price_over_time

def get_total_amount_staked():
  if not nxm_price_over_time:
    get_nxm_token_price()

  times = []
  tree = IntervalTree()
  staking_transactions = query_table('StakingTransactions')
  for txn in staking_transactions:
    times.append(txn['start_time'])
    times.append(txn['end_time'])
    tree[txn['start_time']:txn['end_time']] = txn['amount']

  total_amount_staked = {}
  for time in times:
    if datetime.now() > datetime.strptime(time, '%Y-%m-%d %H:%M:%S'):
      intervals = tree[time]
      total_amount_staked[time] = sum([interval.data for interval in intervals]) * price['NXM']
  return total_amount_staked

def get_amount_staked_per_contract():
  if not nxm_price_over_time:
    get_nxm_token_price()

  amount_per_contract = defaultdict(int)
  staking_transactions = query_table('StakingTransactions')
  for txn in staking_transactions:
    if datetime.now() < datetime.strptime(txn['end_time'], '%Y-%m-%d %H:%M:%S'):
      amount_per_contract[txn['contract_name']] += txn['amount'] * price['NXM']
  return dict(amount_per_contract)

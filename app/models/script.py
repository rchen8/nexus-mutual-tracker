from .models import Cover, Transaction, StakingTransaction
from .utils import get_historical_crypto_price, price, query_table, set_current_crypto_prices
from collections import defaultdict
from datetime import datetime, timedelta
from intervaltree import IntervalTree
import bisect

MINIMUM_CAPITAL_REQUIREMENT = 7000

capital_pool_size = {'USD': {}, 'ETH': {}}
mcr_percentage = {}
nxm_price = {'USD': {}, 'ETH': {}}

def get_active_cover_amount():
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

def get_active_cover_amount_per_contract():
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

def get_all_covers():
  if not price:
    set_current_crypto_prices()

  covers = query_table(Cover)
  for cover in covers:
    cover['start_time'] = cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['end_time'] = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['amount_usd'] = cover['amount'] * price[cover['currency']]
  return covers

def get_capital_pool_size():
  if capital_pool_size['USD'] and capital_pool_size['ETH']:
    return capital_pool_size

  txns = query_table(Transaction)
  txns.sort(key=lambda x: x['timestamp'])
  total = defaultdict(int)
  for txn in txns:
    total[txn['currency']] += txn['amount']
    eth_price = get_historical_crypto_price('ETH', txn['timestamp'])
    dai_price = get_historical_crypto_price('DAI', txn['timestamp'])

    capital_pool_size['USD'][txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total['ETH'] * eth_price + total['DAI'] * dai_price
    capital_pool_size['ETH'][txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total['ETH'] + total['DAI'] / (eth_price / dai_price)
  return capital_pool_size

def get_capital_pool_distribution():
  if not price:
    set_current_crypto_prices()

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
  for time in capital_pool_size['ETH']:
    if capital_pool_size['ETH'][time] > MINIMUM_CAPITAL_REQUIREMENT:
      mcr_percentage[time] = capital_pool_size['ETH'][time] / MINIMUM_CAPITAL_REQUIREMENT * 100
  return mcr_percentage

def get_nxm_token_price():
  if nxm_price['USD'] and nxm_price['ETH']:
    return nxm_price

  A = 1028 / 10**5
  C = 5800000
  get_mcr_percentage()
  for time in mcr_percentage:
    eth_price = get_historical_crypto_price('ETH', datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
    nxm_price['USD'][time] = \
        (A + (MINIMUM_CAPITAL_REQUIREMENT / C) * (mcr_percentage[time] / 100)**4) * eth_price
    nxm_price['ETH'][time] = \
        A + (MINIMUM_CAPITAL_REQUIREMENT / C) * (mcr_percentage[time] / 100)**4
  price['NXM'] = nxm_price['USD'][max(nxm_price['USD'])]
  return nxm_price

def get_total_amount_staked():
  get_nxm_token_price()
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

def get_amount_staked_per_contract():
  get_nxm_token_price()
  amount_staked_per_contract = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for txn in query_table(StakingTransaction):
    if datetime.now() < txn['end_time']:
      amount_staked_per_contract['USD'][txn['contract_name']] += txn['amount'] * price['NXM']
      amount_staked_per_contract['NXM'][txn['contract_name']] += txn['amount']
  return dict(amount_staked_per_contract)

def get_all_stakes():
  get_nxm_token_price()
  stakes = query_table(StakingTransaction)
  for stake in stakes:
    stake['start_time'] = stake['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    stake['end_time'] = stake['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    stake['amount_usd'] = stake['amount'] * price['NXM']
  return stakes

from .. import db, r
from .models import *
from .utils import *
from collections import defaultdict
from datetime import datetime, timedelta
from intervaltree import IntervalTree
import bisect
import json

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

  cover_amount_per_contract = {'USD': defaultdict(int), 'ETH': defaultdict(int)}
  for cover in query_table(Cover):
    if datetime.now() < cover['end_time']:
      cover_amount_per_contract['USD'][cover['contract_name']] += \
          cover['amount'] * float(r.get(cover['currency']))
      cover_amount_per_contract['ETH'][cover['contract_name']] += cover['amount'] / \
          (1 if cover['currency'] == 'ETH' else float(r.get('ETH')) / float(r.get('DAI')))
  return dict(cover_amount_per_contract)

def get_active_cover_amount_by_expiration_date(cache=False):
  if cache:
    return json.loads(r.get('cover_amount_by_expiration_date'))

  cover_amount_by_expiration_date = {'USD': defaultdict(int), 'ETH': defaultdict(int)}
  covers = query_table(Cover)

  last_cover_amount_usd = 0
  last_cover_amount_eth = 0
  for cover in covers:
    if datetime.now() < cover['end_time']:
      last_cover_amount_usd += cover['amount'] * float(r.get(cover['currency']))
      last_cover_amount_eth += cover['amount'] / \
          (1 if cover['currency'] == 'ETH' else float(r.get('ETH')) / float(r.get('DAI')))

  covers.sort(key=lambda x: x['end_time'])
  for cover in covers:
    if datetime.now() < cover['end_time']:
      last_cover_amount_usd -= cover['amount'] * float(r.get(cover['currency']))
      last_cover_amount_eth -= cover['amount'] / \
          (1 if cover['currency'] == 'ETH' else float(r.get('ETH')) / float(r.get('DAI')))
      if last_cover_amount_usd < 0.01:
        last_cover_amount_usd = 0
      if last_cover_amount_eth < 0.01:
        last_cover_amount_eth = 0

      end_time = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
      cover_amount_by_expiration_date['USD'][end_time] = last_cover_amount_usd
      cover_amount_by_expiration_date['ETH'][end_time] = last_cover_amount_eth
  return dict(cover_amount_by_expiration_date)

def get_premiums_paid(cache=False):
  if cache:
    return json.loads(r.get('premiums_paid'))

  total_eth = 0
  total_dai = 0
  premiums_paid = {'USD': {}, 'ETH': {}}
  for cover in query_table(Cover, order=Cover.block_number):
    if cover['currency'] == 'ETH':
      total_eth += cover['premium']
    else:
      total_dai += cover['premium']

    eth_price = get_historical_crypto_price('ETH', cover['start_time'])
    dai_price = get_historical_crypto_price('DAI', cover['start_time'])
    premiums_paid['USD'][cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total_eth * eth_price + total_dai * dai_price
    premiums_paid['ETH'][cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')] = \
        total_eth + total_dai / (eth_price / dai_price)
  return premiums_paid

def get_premiums_paid_per_contract(cache=False):
  if cache:
    return json.loads(r.get('premiums_paid_per_contract'))

  premiums_paid_per_contract = {'USD': defaultdict(int), 'ETH': defaultdict(int)}
  for cover in query_table(Cover):
    premiums_paid_per_contract['USD'][cover['contract_name']] += \
        cover['premium'] * float(r.get(cover['currency']))
    premiums_paid_per_contract['ETH'][cover['contract_name']] += cover['premium'] / \
        (1 if cover['currency'] == 'ETH' else float(r.get('ETH')) / float(r.get('DAI')))
  return dict(premiums_paid_per_contract)  

def get_all_covers(cache=False):
  if cache:
    return json.loads(r.get('covers'))

  covers = query_table(Cover)
  for cover in covers:
    cover['start_time'] = cover['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['end_time'] = cover['end_time'].strftime('%Y-%m-%d %H:%M:%S')
    cover['amount_usd'] = cover['amount'] * float(r.get(cover['currency']))
    cover['premium_usd'] = cover['premium'] * float(r.get(cover['currency']))
  return covers

def get_all_claims(cache=False):
  if cache:
    return json.loads(r.get('claims'))

  covers = sorted(get_all_covers(cache=True), key=lambda x: x['cover_id'])
  claims = query_table(Claim)
  for claim in claims:
    claim['contract_name'] = covers[claim['cover_id'] - 1]['contract_name']
    claim['amount_usd'] = covers[claim['cover_id'] - 1]['amount_usd']
    claim['amount'] = covers[claim['cover_id'] - 1]['amount']
    claim['currency'] = covers[claim['cover_id'] - 1]['currency']
    claim['start_time'] = covers[claim['cover_id'] - 1]['start_time']
    claim['timestamp'] = claim['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
  return claims

def get_all_votes(cache=False):
  if cache:
    return json.loads(r.get('votes'))

  votes = {'USD': {}, 'NXM': {}}
  for vote in query_table(Vote):
    if 'Claim {:02d}'.format(vote['claim_id']) not in votes['USD']:
      votes['USD']['Claim {:02d}'.format(vote['claim_id'])] = {'Yes': 0, 'No': 0}
      votes['NXM']['Claim {:02d}'.format(vote['claim_id'])] = {'Yes': 0, 'No': 0}

    votes['USD']['Claim {:02d}'.format(vote['claim_id'])][vote['verdict']] += \
        vote['amount'] * float(r.get('NXM'))
    votes['NXM']['Claim {:02d}'.format(vote['claim_id'])][vote['verdict']] += vote['amount']
  return votes

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

def get_cover_amount_to_capital_pool_ratio(cache=False):
  if cache:
    return json.loads(r.get('cover_amount_to_capital_pool_ratio'))

  cover_amount = get_active_cover_amount(cache=True)['USD']
  capital_pool_size = get_capital_pool_size(cache=True)['USD']
  capital_pool_times = sorted(capital_pool_size.keys())
  cover_amount_to_capital_pool_ratio = {}
  for time in cover_amount:
    cover_amount_to_capital_pool_ratio[time] = cover_amount[time] / \
        capital_pool_size[capital_pool_times[bisect.bisect(capital_pool_times, time) - 1]] * 100
  return cover_amount_to_capital_pool_ratio

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
  r.set('NXM', nxm_price['USD'][max(nxm_price['USD'])])
  return nxm_price

def get_total_amount_staked(cache=False):
  if cache:
    return json.loads(r.get('amount_staked'))

  # Queue staking
  nxm_price = get_nxm_price(cache=True)
  times = []
  tree = IntervalTree()
  for stake in query_table(Stake):
    if stake['timestamp'] < datetime.strptime('2020-06-30 11:31:12', '%Y-%m-%d %H:%M:%S'):
      times.append(stake['timestamp'])
      times.append(stake['timestamp'] + timedelta(days=250))
      tree[stake['timestamp']:stake['timestamp'] + timedelta(days=250)] = stake['amount']

  amount_staked = {'USD': {}, 'NXM': {}}
  nxm_times = sorted(nxm_price['USD'].keys())
  for time in times:
    if time < datetime.strptime('2020-06-30 11:31:12', '%Y-%m-%d %H:%M:%S'):
      intervals = tree[time]
      historical_nxm_price = nxm_price['USD'] \
          [nxm_times[bisect.bisect(nxm_times, time.strftime('%Y-%m-%d %H:%M:%S')) - 1]]

      amount = sum([(interval.end - time).total_seconds() / timedelta(days=250).total_seconds() * \
          interval.data for interval in intervals])
      amount_staked['USD'][time.strftime('%Y-%m-%d %H:%M:%S')] = amount * historical_nxm_price
      amount_staked['NXM'][time.strftime('%Y-%m-%d %H:%M:%S')] = amount

  # Pooled staking
  amount = 0
  for stake in query_table(Stake, order=Stake.timestamp):
    if stake['timestamp'] < datetime.now():
      if stake['timestamp'] > datetime.strptime('2020-06-30 11:31:12', '%Y-%m-%d %H:%M:%S'):
        amount += stake['amount']
      if stake['timestamp'] > datetime.strptime('2020-06-30 12:16:10', '%Y-%m-%d %H:%M:%S'):
        historical_nxm_price = nxm_price['USD'][nxm_times \
            [bisect.bisect(nxm_times, stake['timestamp'].strftime('%Y-%m-%d %H:%M:%S')) - 1]]
        amount_staked['USD'][stake['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = \
            amount * historical_nxm_price
        amount_staked['NXM'][stake['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = amount

  return amount_staked

def get_amount_staked_per_contract(cache=False):
  if cache:
    return json.loads(r.get('amount_staked_per_contract'))

  amount_staked_per_contract = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for stake in query_table(Stake):
    if stake['timestamp'] > datetime.strptime('2020-06-30 11:31:12', '%Y-%m-%d %H:%M:%S') and \
        stake['timestamp'] < datetime.now():
      amount_staked_per_contract['USD'][stake['contract_name']] += \
          stake['amount'] * float(r.get('NXM'))
      amount_staked_per_contract['NXM'][stake['contract_name']] += stake['amount']
  return dict(amount_staked_per_contract)

def get_top_stakers(cache=False):
  if cache:
    return json.loads(r.get('top_stakers'))

  top_stakers = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for stake in query_table(Stake):
    if stake['timestamp'] > datetime.strptime('2020-06-30 11:31:12', '%Y-%m-%d %H:%M:%S') and \
        stake['timestamp'] < datetime.now():
      top_stakers['USD'][stake['staker']] += stake['amount'] * float(r.get('NXM'))
      top_stakers['NXM'][stake['staker']] += stake['amount']
  return dict(top_stakers)

def get_total_staking_reward(cache=False):
  if cache:
    return json.loads(r.get('staking_reward'))

  nxm_price = get_nxm_price(cache=True)
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

  staking_reward_per_contract = {'USD': defaultdict(int), 'NXM': defaultdict(int)}
  for reward in query_table(StakingReward):
    staking_reward_per_contract['USD'][reward['contract_name']] += \
        reward['amount'] * float(r.get('NXM'))
    staking_reward_per_contract['NXM'][reward['contract_name']] += reward['amount']
  return dict(staking_reward_per_contract)

def get_all_stakes(cache=False):
  if cache:
    return json.loads(r.get('stakes'))

  query = """
SELECT s.contract_name,
       s.address,
       sr.amount AS total_reward,
       sum(s.amount) AS total_staked,
       sr.annualized_amount
FROM stake s
INNER JOIN
  (SELECT sr.contract_name,
          sr.address,
          sum(sr.amount) AS amount,
          sum(365 * 86400 / extract(epoch
                                    FROM (end_time - start_time)) * sr.amount) AS annualized_amount
   FROM staking_reward sr
   INNER JOIN cover c ON sr.timestamp = c.start_time
   WHERE TIMESTAMP >= '2020-06-30 11:31:12'
   GROUP BY sr.contract_name,
            sr.address) sr ON s.address = sr.address
WHERE s.timestamp >= '2020-06-30 11:31:12'
  AND s.timestamp <= \'%s\'
GROUP BY s.contract_name,
         s.address,
         sr.amount,
         sr.annualized_amount
""" % datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  all_stakes = []
  for stake in db.engine.execute(query):
    if stake[1] == '0x45f783cce6b7ff23b2ab2d70e416cdb7d6055f51':
      continue
    all_stakes.append({
      'contract_name': stake[0],
      'address': stake[1],
      'total_reward': stake[2],
      'total_reward_usd': stake[2] * float(r.get('NXM')),
      'total_staked': stake[3],
      'total_staked_usd': stake[3] * float(r.get('NXM')),
      'estimated_yield': stake[4] / stake[3] * 100
    })
  return all_stakes

def get_nxm_return_vs_eth(cache=False):
  if cache:
    return json.loads(r.get('nxm_return_vs_eth'))

  start_price = 0.01028
  nxm_price = get_nxm_price(cache=True)['ETH']
  nxm_return_vs_eth = {}
  for time in nxm_price:
    nxm_return_vs_eth[time] = (nxm_price[time] / start_price - 1) * 100
    if abs(nxm_return_vs_eth[time]) < 0.01:
      nxm_return_vs_eth[time] = 0
  return nxm_return_vs_eth

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

  nxm_price = get_nxm_price(cache=True)
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
      nxm_distribution.pop('0x84edffa16bb0b9ab1163abb0a13ff0744c11272f')
  return nxm_distribution

def get_unique_addresses(cache=False):
  if cache:
    return json.loads(r.get('unique_addresses'))

  balances = defaultdict(int)
  unique_addresses = {}
  for txn in query_table(NXMTransaction, order=NXMTransaction.block_number):
    balances[txn['from_address']] -= txn['amount']
    balances[txn['to_address']] += txn['amount']

    if balances[txn['from_address']] < 10**-8:
      del balances[txn['from_address']]
    unique_addresses[txn['timestamp'].strftime('%Y-%m-%d %H:%M:%S')] = len(balances)
  return unique_addresses

def cache_graph_data():
  r.set('cover_amount', json.dumps(get_active_cover_amount(cache=False)))
  r.set('cover_amount_per_contract', json.dumps(get_active_cover_amount_per_contract(cache=False)))
  r.set('cover_amount_by_expiration_date',
      json.dumps(get_active_cover_amount_by_expiration_date(cache=False)))
  r.set('premiums_paid', json.dumps(get_premiums_paid(cache=False)))
  r.set('premiums_paid_per_contract', json.dumps(get_premiums_paid_per_contract(cache=False)))
  r.set('covers', json.dumps(get_all_covers(cache=False)))
  r.set('claims', json.dumps(get_all_claims(cache=False)))
  r.set('capital_pool_size', json.dumps(get_capital_pool_size(cache=False)))
  r.set('cover_amount_to_capital_pool_ratio',
      json.dumps(get_cover_amount_to_capital_pool_ratio(cache=False)))
  r.set('minimum_capital_requirement', json.dumps(get_minimum_capital_requirement(cache=False)))
  r.set('mcr_percentage', json.dumps(get_mcr_percentage(over_100=True, cache=False)))
  r.set('nxm_price', json.dumps(get_nxm_price(cache=False)))
  r.set('votes', json.dumps(get_all_votes(cache=False)))
  r.set('amount_staked', json.dumps(get_total_amount_staked(cache=False)))
  r.set('amount_staked_per_contract', json.dumps(get_amount_staked_per_contract(cache=False)))
  r.set('top_stakers', json.dumps(get_top_stakers(cache=False)))
  r.set('staking_reward', json.dumps(get_total_staking_reward(cache=False)))
  r.set('staking_reward_per_contract', json.dumps(get_staking_reward_per_contract(cache=False)))
  r.set('stakes', json.dumps(get_all_stakes(cache=False)))
  r.set('nxm_return_vs_eth', json.dumps(get_nxm_return_vs_eth(cache=False)))
  r.set('nxm_supply', json.dumps(get_nxm_supply(cache=False)))
  r.set('nxm_market_cap', json.dumps(get_nxm_market_cap(cache=False)))
  r.set('nxm_distribution', json.dumps(get_nxm_distribution(cache=False)))
  r.set('unique_addresses', json.dumps(get_unique_addresses(cache=False)))

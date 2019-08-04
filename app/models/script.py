from collections import defaultdict
from datetime import datetime
from intervaltree import IntervalTree
import json
import os
import requests
import textwrap

MINIMUM_CAPITAL_REQUIREMENT = 7000

covers = []
transactions = []
pool_size_over_time = {}
mcr_percentage_over_time = {}

def get_active_cover_amount():
  times = []
  tree = IntervalTree()
  for cover in covers:
    times.append(cover['start_time'])
    times.append(cover['end_time'])
    tree[cover['start_time']:cover['end_time']] = cover['amount']

  amount_over_time = {}
  for time in times:
    if datetime.now() > time:
      intervals = tree[time]
      amount_over_time[time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data for interval in intervals])
  return amount_over_time

def address_to_contract_name(address):
  names = {
    '514910771af9ca656af840dff83e8264ecf986ca': 'ChainLink',
    '3d9819210a31b4961b30ef54be2aed79b9c9cd3b': 'Compound',
    '4ddc2d193948926d02f9b1fe9e1daa0718270ed5': 'Compound',
    '1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e': 'dYdX',
    '8573f2f5a3bd960eee3d998473e50c75cdbe6828': 'Livepeer',
    '448a5065aebb8e423f0896e6c5d525c040f59af3': 'MakerDAO',
    '9f8f72aa9304c8b593d555f12ef6589cc3a579a2': 'MakerDAO',
    '802275979b020f0ec871c5ec1db6e412b72ff20b': 'Nuo Network',
    'cd2053679de3bcf2b7e2c2efb6b499c57701222c': 'Totle',
    'c0a47dfe034b400b47bdad5fecda2621de6c4d95': 'Uniswap'
  }
  return names[address.lower()] if address.lower() in names else 'Other'

def get_active_cover_amount_per_contract():
  amount_per_contract = defaultdict(int)
  for cover in covers:
    if datetime.now() < cover['end_time']:
      amount_per_contract[address_to_contract_name(cover['address'])] += cover['amount']
  return dict(amount_per_contract)

def get_capital_pool_size():
  transactions.sort(key=lambda x: x['timeStamp'])
  total = 0
  for transaction in transactions:
    total += transaction['amount']
    pool_size_over_time[transaction['timeStamp'].strftime('%Y-%m-%d %H:%M:%S')] = total
  return pool_size_over_time

def get_mcr_percentage():
  if not pool_size_over_time:
    get_capital_pool_size()

  for time in pool_size_over_time:
    if pool_size_over_time[time] / ETH_PRICE > MINIMUM_CAPITAL_REQUIREMENT:
      mcr_percentage_over_time[time] = (pool_size_over_time[time] / ETH_PRICE) / \
          MINIMUM_CAPITAL_REQUIREMENT * 100
  return mcr_percentage_over_time

def get_nxm_token_price():
  if not mcr_percentage_over_time:
    get_mcr_percentage()

  A = 1028 / 10**5
  C = 5800000
  nxm_price_over_time = {}
  for time in mcr_percentage_over_time:
    nxm_price_over_time[time] = \
        (A + (MINIMUM_CAPITAL_REQUIREMENT / C) * (mcr_percentage_over_time[time] / 100)**4) * \
        ETH_PRICE
  return nxm_price_over_time

####################################################################################################

def parse_event_logs(event_logs):
  """
  index_topic_1 uint256 coverage_id
  CoverDetailsEvent (
    address smart_contract_address,
    uint256 coverage_amount,
    uint256 expiry,
    uint256 premium,
    uint256 premiumNXM,
    bytes4 curr
  )
  """
  for event in event_logs:
    data = textwrap.wrap(event['data'][2:], 64)

    amount = float(int(data[1], 16))
    if data[-1].startswith('455448'):
      amount *= ETH_PRICE
    elif data[-1].startswith('444149'):
      amount *= DAI_PRICE
    else:
      raise

    covers.append({
      'address': data[0][-40:],
      'amount': amount,
      'start_time': datetime.fromtimestamp(int(event['timeStamp'], 16)),
      'end_time': datetime.fromtimestamp(int(data[2], 16))
    })

def get_event_logs():
  module = 'logs'
  action = 'getLogs'
  fromBlock = '1'
  toBlock = 'latest'
  address = '0x1776651F58a17a50098d31ba3C3cD259C1903f7A'
  topic0 = '0x535c0318711210e1ce39e443c5948dd7fa396c2774d0949812fcb74800e22730'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s' \
        % (module, action, fromBlock, toBlock, address, topic0, os.getenv('API_KEY'))
  parse_event_logs(json.loads(requests.get(url).text)['result'])

def parse_transactions(txns, address, crypto_price):
  for txn in txns:
    if 'isError' not in txn or txn['isError'] == '0':
      amount = float(txn['value']) / 10**18 * crypto_price
      if txn['from'].lower() == address.lower():
        amount = -amount

      if amount != 0:
        transactions.append({
          'timeStamp': datetime.fromtimestamp(int(txn['timeStamp'])),
          'amount': amount
        })

def get_eth_transactions():
  # Normal transactions
  module = 'account'
  action = 'txlist'
  address = '0xfD61352232157815cF7B71045557192Bf0CE1884'
  startblock = '1'
  endblock = 'latest'
  sort = 'asc'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&address=%s&startblock=%s&endblock=%s&sort=%s&apikey=%s' \
        % (module, action, address, startblock, endblock, sort, os.getenv('API_KEY'))
  parse_transactions(json.loads(requests.get(url).text)['result'], address, ETH_PRICE)

  # Internal transactions
  url = url.replace('txlist', 'txlistinternal')
  parse_transactions(json.loads(requests.get(url).text)['result'], address, ETH_PRICE)

def get_dai_transactions():
  module = 'account'
  action = 'tokentx'
  contractaddress = '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359'
  address = '0xfD61352232157815cF7B71045557192Bf0CE1884'
  sort = 'asc'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&contractaddress=%s&address=%s&sort=%s&apikey=%s' \
        % (module, action, contractaddress, address, sort, os.getenv('API_KEY'))
  parse_transactions(json.loads(requests.get(url).text)['result'], address, DAI_PRICE)

def get_crypto_price(currency):
  return float(json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/%s' % currency) \
      .text)[0]['price_usd'])

def get_etherscan_data():
  global ETH_PRICE, DAI_PRICE
  ETH_PRICE = get_crypto_price('ethereum')
  DAI_PRICE = get_crypto_price('dai')

  covers.clear()
  transactions.clear()
  get_event_logs()
  get_eth_transactions()
  get_dai_transactions()

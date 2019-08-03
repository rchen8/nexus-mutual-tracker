from collections import defaultdict
from datetime import datetime
from intervaltree import IntervalTree
import json
import os
import requests
import textwrap

covers = []

def address_to_contract_name(address):
  names = {
    '514910771af9ca656af840dff83e8264ecf986ca': 'ChainLink',
    '3d9819210a31b4961b30ef54be2aed79b9c9cd3b': 'Compound',
    '4ddc2d193948926d02f9b1fe9e1daa0718270ed5': 'Compound',
    '1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e': 'dYdX',
    '448a5065aebb8e423f0896e6c5d525c040f59af3': 'MakerDAO',
    '9f8f72aa9304c8b593d555f12ef6589cc3a579a2': 'MakerDAO',
    '802275979b020f0ec871c5ec1db6e412b72ff20b': 'Nuo Network',
    'cd2053679de3bcf2b7e2c2efb6b499c57701222c': 'Totle',
    'c0a47dfe034b400b47bdad5fecda2621de6c4d95': 'Uniswap'
  }
  return names[address] if address in names else 'Other'

def get_cover_amount_per_contract():
  amount_per_contract = defaultdict(int)
  for cover in covers:
    if datetime.now() < cover['end_time']:
      amount_per_contract[address_to_contract_name(cover['address'])] += cover['amount']
  return dict(amount_per_contract)

def get_cover_amount_over_time():
  times = []
  tree = IntervalTree()
  for cover in covers:
    times.append(cover['start_time'])
    times.append(cover['end_time'])
    tree[cover['start_time']:cover['end_time']] = cover['amount']

  amount_per_time = {}
  for time in times:
    if datetime.now() > time:
      intervals = tree[time]
      amount_per_time[time.strftime('%Y-%m-%d %H:%M:%S')] = \
          sum([interval.data for interval in intervals])
  return amount_per_time

def get_crypto_price(currency):
  return float(json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/%s' % currency) \
      .text)[0]['price_usd'])

def parse_data(raw_data):
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
  covers.clear()
  eth_price = get_crypto_price('ethereum')
  dai_price = get_crypto_price('dai')
  for item in raw_data:
    data = textwrap.wrap(item['data'][2:], 64)

    amount = float(int(data[1], 16))
    if data[-1].startswith('455448'):
      amount *= eth_price
    elif data[-1].startswith('444149'):
      amount *= dai_price
    else:
      raise

    covers.append({
      'address': data[0][-40:],
      'amount': amount,
      'start_time': datetime.fromtimestamp(int(item['timeStamp'], 16)),
      'end_time': datetime.fromtimestamp(int(data[2], 16))
    })

def get_etherscan_data():
  module = 'logs'
  action = 'getLogs'
  fromBlock = '1'
  toBlock = 'latest'
  address = '0x1776651F58a17a50098d31ba3C3cD259C1903f7A'
  topic0 = '0x535c0318711210e1ce39e443c5948dd7fa396c2774d0949812fcb74800e22730'
  url = 'https://api.etherscan.io/api?module=%s&action=%s&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s' \
      % (module, action, fromBlock, toBlock, address, topic0, os.getenv('API_KEY'))
  
  parse_data(json.loads(requests.get(url).text)['result'])

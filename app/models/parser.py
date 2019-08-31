from .utils import address_to_contract_name, price, set_crypto_prices
from .script import covers, staking_transactions, transactions
from datetime import datetime, timedelta
import json
import os
import requests
import textwrap

def get_event_logs():
  module = 'logs'
  action = 'getLogs'
  fromBlock = '1'
  toBlock = 'latest'
  address = '0x1776651F58a17a50098d31ba3C3cD259C1903f7A'
  topic0 = '0x535c0318711210e1ce39e443c5948dd7fa396c2774d0949812fcb74800e22730'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s' \
        % (module, action, fromBlock, toBlock, address, topic0, os.environ['ETHERSCAN_API_KEY'])
  return json.loads(requests.get(url).text)['result']

def parse_event_logs():
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
  event_logs = get_event_logs()
  for event in event_logs:
    data = textwrap.wrap(event['data'][2:], 64)

    amount = float(int(data[1], 16))
    if data[-1].startswith('455448'):
      amount *= price['ETH']
    elif data[-1].startswith('444149'):
      amount *= price['DAI']
    else:
      raise

    covers.append({
      'id': int(event['topics'][1], 16),
      'contract_name': address_to_contract_name(data[0][-40:]),
      'amount': amount,
      'start_time': datetime.fromtimestamp(int(event['timeStamp'], 16)),
      'end_time': datetime.fromtimestamp(int(data[2], 16))
    })

def parse_transactions(txns, address, crypto_price):
  for txn in txns:
    if 'isError' not in txn or txn['isError'] == '0':
      amount = float(txn['value']) / 10**18 * crypto_price
      if txn['from'].lower() == address.lower():
        amount = -amount

      if amount != 0:
        transactions.append({
          'timeStamp': datetime.fromtimestamp(int(txn['timeStamp'])),
          'from_address': txn['from'],
          'to_address': txn['to'],
          'amount': amount
        })

def build_transaction_url(address):
  module = 'account'
  action = 'txlist'
  startblock = '1'
  endblock = 'latest'
  sort = 'asc'
  return 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&address=%s&startblock=%s&endblock=%s&sort=%s&apikey=%s' \
        % (module, action, address, startblock, endblock, sort, os.environ['ETHERSCAN_API_KEY'])

def parse_eth_transactions():
  address = '0xfD61352232157815cF7B71045557192Bf0CE1884'
  url = build_transaction_url(address)
  parse_transactions(json.loads(requests.get(url).text)['result'], address, price['ETH'])
  url = url.replace('txlist', 'txlistinternal')
  parse_transactions(json.loads(requests.get(url).text)['result'], address, price['ETH'])

def parse_dai_transactions():
  module = 'account'
  action = 'tokentx'
  contractaddress = '0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359'
  address = '0xfD61352232157815cF7B71045557192Bf0CE1884'
  sort = 'asc'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&contractaddress=%s&address=%s&sort=%s&apikey=%s' \
        % (module, action, contractaddress, address, sort, os.environ['ETHERSCAN_API_KEY'])
  parse_transactions(json.loads(requests.get(url).text)['result'], address, price['DAI'])

def parse_staking_transactions():
  url = build_transaction_url('0xDF50A17bF58dea5039B73683a51c4026F3c7224E')
  txns = json.loads(requests.get(url).text)['result']
  for txn in txns:
    if txn['isError'] == '0':
      data = textwrap.wrap(txn['input'][10:], 64)
      if len(data) == 2:
        start_time = datetime.fromtimestamp(int(txn['timeStamp']))
        staking_transactions.append({
          'start_time': start_time,
          'end_time': start_time + timedelta(days=250),
          'contract_name': address_to_contract_name(data[0][-40:]),
          'amount': float(int(data[1], 16)) / 10**18
        })

def parse_etherscan_data():
  covers.clear()
  transactions.clear()
  staking_transactions.clear()

  set_crypto_prices()
  parse_event_logs()
  parse_eth_transactions()
  parse_dai_transactions()
  parse_staking_transactions()

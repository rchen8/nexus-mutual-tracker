from .. import db
from .models import *
from .utils import *
from datetime import datetime, timedelta
import json
import os
import requests
import textwrap

def get_event_logs(table, address, topic0):
  module = 'logs'
  action = 'getLogs'
  fromBlock = get_latest_block_number(table) + 1
  toBlock = 'latest'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s' \
        % (module, action, fromBlock, toBlock, address, topic0, os.environ['ETHERSCAN_API_KEY'])
  return json.loads(requests.get(url).text)['result']

def parse_cover_event_logs():
  address = '0x1776651f58a17a50098d31ba3c3cd259c1903f7a'
  topic0 = '0x535c0318711210e1ce39e443c5948dd7fa396c2774d0949812fcb74800e22730'
  for event in get_event_logs(Cover, address, topic0):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Cover(
      block_number=int(event['blockNumber'], 16),
      cover_id=int(event['topics'][1], 16),
      contract_name=address_to_contract_name(data[0][-40:]),
      amount=float(int(data[1], 16)),
      premium=float(int(data[3], 16)) / 10**18,
      currency='ETH' if data[-1].startswith('455448') else 'DAI',
      start_time=datetime.fromtimestamp(int(event['timeStamp'], 16)),
      end_time=datetime.fromtimestamp(int(data[2], 16))
    ))
  db.session.commit()

def parse_claim_event_logs():
  address = '0xdc2d359f59f6a26162972c3bd0cfbfd8c9ef43af'
  topic0 = '0x040b2cc991821ffe51dd33e7f7a2d0e6f64d2ad487cdabbf9e8c1805a93028c4'
  for event in get_event_logs(Claim, address, topic0):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Claim(
      block_number=int(event['blockNumber'], 16),
      claim_id=int(data[0], 16),
      cover_id=int(event['topics'][1], 16),
      date=datetime.fromtimestamp(int(data[1], 16))
    ))
  db.session.commit()

def parse_verdict_event_logs():
  address = '0x1776651f58a17a50098d31ba3c3cd259c1903f7a'
  topic0 = '0x7f1cec39abbda212a819b9165ccfc4064f73eb454b052a312807b2270067a53d'
  for event in get_event_logs(None, address, topic0):
    if int(event['data'], 16) == 1:
      Claim.query.filter_by(cover_id=int(event['topics'][1], 16)).\
          filter(Claim.block_number < int(event['blockNumber'], 16)).\
          order_by(Claim.block_number.desc()).first().verdict = 'Accepted'
    elif int(event['data'], 16) == 2:
      claim = Claim.query.filter_by(cover_id=int(event['topics'][1], 16)).\
          filter(Claim.block_number < int(event['blockNumber'], 16)).\
          order_by(Claim.block_number.desc()).first().verdict = 'Denied'
  db.session.commit()

def parse_vote_event_logs():
  address = '0xdc2d359f59f6a26162972c3bd0cfbfd8c9ef43af'
  topic0 = '0xccc99158fb6c7b960e4d6e873692c8e8f8785c44da681aad285f3251940840d9'
  for event in get_event_logs(Vote, address, topic0):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Vote(
      id=get_last_id(Vote) + 1,
      block_number=int(event['blockNumber'], 16),
      claim_id=int(event['topics'][2], 16),
      amount=int(data[0], 16) / 10**18,
      date=datetime.fromtimestamp(int(data[1], 16)),
      verdict='Yes' if int(data[2], 16) == 1 else 'No'
    ))
  db.session.commit()

def parse_mcr_event_logs():
  address = '0x2ec5d566bd104e01790b13de33fd51876d57c495'
  topic0 = '0xe4d7c0f9c1462bca57d9d1c2ec3a19d83c4781ceaf9a37a0f15dc55a6b43de4d'
  for event in get_event_logs(MinimumCapitalRequirement, address, topic0):
    db.session.add(MinimumCapitalRequirement(
      timestamp=datetime.fromtimestamp(int(event['timeStamp'], 16)),
      block_number=int(event['blockNumber'], 16),
      mcr=int(textwrap.wrap(event['data'][2:], 64)[3], 16) / 10**18
    ))
  db.session.commit()

def parse_staking_event_logs():
  address='0xe20b3ae826cdb43676e418f7c3b84b75b5697a40'
  topic0 = '0x05456de91d83e21ad7c41a09ae7cb41836049c49e6ddaf07bdfc40c2231885d2'
  for event in get_event_logs(StakingReward, address, topic0):
    db.session.add(StakingReward(
      id=get_last_id(StakingReward) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.fromtimestamp(int(event['timeStamp'], 16)),
      staker='0x' + event['topics'][1][-40:],
      contract_name=address_to_contract_name(event['topics'][2][-40:]),
      amount=int(event['data'], 16) / 10**18
    ))
  db.session.commit()

def parse_nxm_event_logs():
  address = '0xd7c49cee7e9188cca6ad8ff264c1da2e69d4cf3b'
  topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
  for event in get_event_logs(NXMTransaction, address, topic0):
    db.session.add(NXMTransaction(
      id=get_last_id(NXMTransaction) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.fromtimestamp(int(event['timeStamp'], 16)),
      from_address='0x' + event['topics'][1][-40:],
      to_address='0x' + event['topics'][2][-40:],
      amount=int(event['data'], 16) / 10**18
    ))
  db.session.commit()

def parse_transactions(txns, address, symbol):
  for txn in txns:
    if 'isError' not in txn or txn['isError'] == '0':
      amount = float(txn['value']) / 10**18
      if txn['from'].lower() == address.lower():
        amount = -amount

      if amount != 0:
        timestamp = datetime.fromtimestamp(int(txn['timeStamp']))
        db.session.add(Transaction(
          id=get_last_id(Transaction) + 1,
          block_number=txn['blockNumber'],
          timestamp=timestamp,
          from_address=txn['from'],
          to_address=txn['to'],
          amount=amount,
          currency=symbol
        ))
  db.session.commit()

def build_transaction_url(address, startblock):
  module = 'account'
  action = 'txlist'
  endblock = 'latest'
  sort = 'asc'
  return 'https://api.etherscan.io/api?' + \
         'module=%s&action=%s&address=%s&startblock=%s&endblock=%s&sort=%s&apikey=%s' \
         % (module, action, address, startblock, endblock, sort, os.environ['ETHERSCAN_API_KEY'])

def parse_eth_transactions(startblock):
  addresses = ['0xfd61352232157815cf7b71045557192bf0ce1884',
               '0x7cbe5682be6b648cc1100c76d4f6c96997f753d6']
  for address in addresses:
    url = build_transaction_url(address, startblock)
    parse_transactions(json.loads(requests.get(url).text)['result'], address, 'ETH')
    url = url.replace('txlist', 'txlistinternal')
    parse_transactions(json.loads(requests.get(url).text)['result'], address, 'ETH')

def parse_dai_transactions(startblock):
  addresses = ['0xfd61352232157815cf7b71045557192bf0ce1884',
               '0x7cbe5682be6b648cc1100c76d4f6c96997f753d6']
  for address in addresses:
    module = 'account'
    action = 'tokentx'
    contractaddress = '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359'
    endblock = 'latest'
    sort = 'asc'
    url = ('https://api.etherscan.io/api?module=%s&action=%s&contractaddress=%s&address=%s&' + \
          'startblock=%s&endblock=%s&sort=%s&apikey=%s') \
          % (module, action, contractaddress, address,
          startblock, endblock, sort, os.environ['ETHERSCAN_API_KEY'])
    parse_transactions(json.loads(requests.get(url).text)['result'], address, 'DAI')

def parse_staking_transactions():
  startblock = get_latest_block_number(StakingTransaction) + 1
  url = build_transaction_url('0xdf50a17bf58dea5039b73683a51c4026f3c7224e', startblock)
  for txn in json.loads(requests.get(url).text)['result']:
    if txn['isError'] == '0':
      data = textwrap.wrap(txn['input'][10:], 64)
      if len(data) == 2:
        start_time = datetime.fromtimestamp(int(txn['timeStamp']))
        db.session.add(StakingTransaction(
          id=get_last_id(StakingTransaction) + 1,
          block_number=txn['blockNumber'],
          start_time=start_time,
          end_time=start_time + timedelta(days=250),
          contract_name=address_to_contract_name(data[0][-40:]),
          address='0x' + data[0][-40:],
          amount=float(int(data[1], 16)) / 10**18
        ))
  db.session.commit()

def parse_etherscan_data():
  set_current_crypto_prices()

  parse_cover_event_logs()
  parse_claim_event_logs()
  parse_verdict_event_logs()
  parse_vote_event_logs()

  parse_mcr_event_logs()
  parse_staking_event_logs()
  parse_nxm_event_logs()

  startblock = get_latest_block_number(Transaction) + 1
  parse_eth_transactions(startblock)
  parse_dai_transactions(startblock)
  parse_staking_transactions()

from .. import db
from .models import *
from .utils import *
from datetime import datetime
import os
import requests
import textwrap
import time

def get_event_logs(table, address, topic0, from_block=None, to_block='latest'):
  if from_block is None:
    from_block = get_latest_block_number(table) + 1

  time.sleep(0.2)
  module = 'logs'
  action = 'getLogs'
  url = 'https://api.etherscan.io/api?' + \
        'module=%s&action=%s&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s' \
        % (module, action, from_block, to_block, address, topic0, os.environ['ETHERSCAN_API_KEY'])
  return requests.get(url).json()['result']

def parse_cover_event_logs(to_block):
  address = '0x1776651f58a17a50098d31ba3c3cd259c1903f7a'
  topic0 = '0x535c0318711210e1ce39e443c5948dd7fa396c2774d0949812fcb74800e22730'
  for event in get_event_logs(Cover, address, topic0, to_block=to_block):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Cover(
      block_number=int(event['blockNumber'], 16),
      cover_id=int(event['topics'][1], 16),
      project=address_to_project(data[0][-40:]),
      address='0x' + data[0][-40:],
      amount=float(int(data[1], 16)),
      premium=float(int(data[3], 16)) / 10**18,
      currency='ETH' if data[-1].startswith('455448') else 'DAI',
      start_time=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      end_time=datetime.utcfromtimestamp(int(data[2], 16))
    ))

def parse_claim_event_logs(to_block):
  address = '0xdc2d359f59f6a26162972c3bd0cfbfd8c9ef43af'
  topic0 = '0x040b2cc991821ffe51dd33e7f7a2d0e6f64d2ad487cdabbf9e8c1805a93028c4'
  for event in get_event_logs(Claim, address, topic0, to_block=to_block):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Claim(
      block_number=int(event['blockNumber'], 16),
      claim_id=int(data[0], 16),
      cover_id=int(event['topics'][1], 16),
      timestamp=datetime.utcfromtimestamp(int(data[1], 16))
    ))

def parse_verdict_event_logs(to_block):
  address = '0x1776651f58a17a50098d31ba3c3cd259c1903f7a'
  topic0 = '0x7f1cec39abbda212a819b9165ccfc4064f73eb454b052a312807b2270067a53d'
  from_block = Claim.query.filter_by(verdict='Pending').\
      order_by(Claim.block_number).first()
  if from_block is None:
    return

  for event in get_event_logs(Claim, address, topic0, from_block.block_number, to_block):
    verdict = int(event['data'], 16)
    if verdict in [1, 2]:
      claim = Claim.query.filter_by(cover_id=int(event['topics'][1], 16)).\
          filter(Claim.block_number < int(event['blockNumber'], 16)).\
          order_by(Claim.block_number.desc()).first()
      claim.verdict = 'Accepted' if verdict == 1 else 'Denied'

def parse_vote_event_logs(to_block):
  address = '0xdc2d359f59f6a26162972c3bd0cfbfd8c9ef43af'
  topic0 = '0xccc99158fb6c7b960e4d6e873692c8e8f8785c44da681aad285f3251940840d9'
  for event in get_event_logs(Vote, address, topic0, to_block=to_block):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Vote(
      id=get_last_id(Vote) + 1,
      block_number=int(event['blockNumber'], 16),
      claim_id=int(event['topics'][2], 16),
      amount=int(data[0], 16) / 10**18,
      timestamp=datetime.utcfromtimestamp(int(data[1], 16)),
      verdict='Yes' if int(data[2], 16) == 1 else 'No'
    ))

def parse_mcr_event_logs(to_block):
  address = '0x2ec5d566bd104e01790b13de33fd51876d57c495'
  topic0 = '0xe4d7c0f9c1462bca57d9d1c2ec3a19d83c4781ceaf9a37a0f15dc55a6b43de4d'
  for event in get_event_logs(MinimumCapitalRequirement, address, topic0, to_block=to_block):
    db.session.add(MinimumCapitalRequirement(
      timestamp=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      block_number=int(event['blockNumber'], 16),
      mcr=int(textwrap.wrap(event['data'][2:], 64)[3], 16) / 10**18
    ))

def parse_stake_event_logs(from_block, to_block):
  address = '0x84edffa16bb0b9ab1163abb0a13ff0744c11272f'
  topic0 = '0x5dac0c1b1112564a045ba943c9d50270893e8e826c49be8e7073adc713ab7bd7'
  for event in get_event_logs(Stake, address, topic0, from_block, to_block):
    db.session.add(Stake(
      id=get_last_id(Stake) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      staker='0x' + event['topics'][2][-40:],
      project=address_to_project(event['topics'][1][-40:]),
      address='0x' + event['topics'][1][-40:],
      amount=int(event['data'], 16) / 10**18
    ))

def parse_unstake_event_logs(from_block, to_block):
  address = '0x84edffa16bb0b9ab1163abb0a13ff0744c11272f'
  topic0 = '0xfe07ce9fff39f8420b3de5fbc6909ce08f809e2572b62f9df35c25f56d610bb0'
  for event in get_event_logs(Stake, address, topic0, from_block, to_block):
    data = textwrap.wrap(event['data'][2:], 64)
    db.session.add(Stake(
      id=get_last_id(Stake) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.utcfromtimestamp(int(data[1], 16)),
      staker='0x' + event['topics'][2][-40:],
      project=address_to_project(event['topics'][1][-40:]),
      address='0x' + event['topics'][1][-40:],
      amount=-int(data[0], 16) / 10**18
    ))

def parse_staking_reward_event_logs(to_block):
  address = '0xe20b3ae826cdb43676e418f7c3b84b75b5697a40'
  topic0 = '0x05456de91d83e21ad7c41a09ae7cb41836049c49e6ddaf07bdfc40c2231885d2'
  for event in get_event_logs(StakingReward, address, topic0, to_block=to_block):
    db.session.add(StakingReward(
      id=get_last_id(StakingReward) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      project=address_to_project(event['topics'][2][-40:]),
      address='0x' + event['topics'][2][-40:],
      amount=int(event['data'], 16) / 10**18
    ))

  address = '0x84edffa16bb0b9ab1163abb0a13ff0744c11272f'
  topic0 = '0x5f5b850fcbd0c09e2b8624b44902a5be89312011ae945e14bc73514fb719891e'
  for event in get_event_logs(StakingReward, address, topic0, to_block=to_block):
    db.session.add(StakingReward(
      id=get_last_id(StakingReward) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      project=address_to_project(event['topics'][1][-40:]),
      address='0x' + event['topics'][1][-40:],
      amount=int(event['data'], 16) / 10**18
    ))

def parse_nxm_event_logs(to_block):
  address = '0xd7c49cee7e9188cca6ad8ff264c1da2e69d4cf3b'
  topic0 = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
  for event in get_event_logs(NXMTransaction, address, topic0, to_block=to_block):
    db.session.add(NXMTransaction(
      id=get_last_id(NXMTransaction) + 1,
      block_number=int(event['blockNumber'], 16),
      timestamp=datetime.utcfromtimestamp(int(event['timeStamp'], 16)),
      from_address='0x' + event['topics'][1][-40:],
      to_address='0x' + event['topics'][2][-40:],
      amount=int(event['data'], 16) / 10**18
    ))

def parse_transactions(txns, address, symbol):
  for txn in txns:
    if 'isError' in txn and txn['isError'] == '1':
      continue

    amount = float(txn['value']) / 10**18
    if txn['from'].lower() == address.lower():
      amount = -amount

    if amount != 0:
      timestamp = datetime.utcfromtimestamp(int(txn['timeStamp']))
      db.session.add(Transaction(
        id=get_last_id(Transaction) + 1,
        block_number=txn['blockNumber'],
        timestamp=timestamp,
        from_address=txn['from'],
        to_address=txn['to'],
        amount=amount,
        currency=symbol
      ))

def build_transaction_url(address, start_block, end_block='latest'):
  module = 'account'
  action = 'txlist'
  sort = 'asc'
  return 'https://api.etherscan.io/api?' + \
         'module=%s&action=%s&address=%s&startblock=%s&endblock=%s&sort=%s&apikey=%s' \
         % (module, action, address, start_block, end_block, sort, os.environ['ETHERSCAN_API_KEY'])

def parse_eth_transactions(start_block, end_block):
  addresses = ['0xfd61352232157815cf7b71045557192bf0ce1884',
               '0x7cbe5682be6b648cc1100c76d4f6c96997f753d6']
  for address in addresses:
    url = build_transaction_url(address, start_block, end_block)
    time.sleep(0.2)
    parse_transactions(requests.get(url).json()['result'], address, 'ETH')
    url = url.replace('txlist', 'txlistinternal')
    time.sleep(0.2)
    parse_transactions(requests.get(url).json()['result'], address, 'ETH')

def parse_dai_transactions(start_block, end_block):
  addresses = ['0xfd61352232157815cf7b71045557192bf0ce1884',
               '0x7cbe5682be6b648cc1100c76d4f6c96997f753d6']
  for address in addresses:
    time.sleep(0.2)
    module = 'account'
    action = 'tokentx'
    contract_address = '0x6b175474e89094c44da98b954eedeac495271d0f'
    sort = 'asc'
    url = ('https://api.etherscan.io/api?module=%s&action=%s&contractaddress=%s&address=%s&' + \
          'startblock=%s&endblock=%s&sort=%s&apikey=%s') \
          % (module, action, contract_address, address,
          start_block, end_block, sort, os.environ['ETHERSCAN_API_KEY'])
    parse_transactions(requests.get(url).json()['result'], address, 'DAI')

def parse_staking_transactions(end_block):
  start_block = get_latest_block_number(Stake) + 1
  addresses = ['0xdf50a17bf58dea5039b73683a51c4026f3c7224e',
               '0xa94c7e87e212669baee95d5d45305d05e6b8a28f']
  for address in addresses:
    url = build_transaction_url(address, start_block, end_block)
    time.sleep(0.2)
    for txn in requests.get(url).json()['result']:
      if txn['isError'] == '0':
        data = textwrap.wrap(txn['input'][10:], 64)
        if len(data) == 2:
          amount = float(int(data[1], 16)) / 10**18
          if amount >= 10**-8:
            db.session.add(Stake(
              id=get_last_id(Stake) + 1,
              block_number=txn['blockNumber'],
              timestamp=datetime.utcfromtimestamp(int(txn['timeStamp'])),
              staker=txn['from'],
              project=address_to_project(data[0][-40:]),
              address='0x' + data[0][-40:],
              amount=amount
            ))

def parse_etherscan_data():
  to_block = get_to_block()
  parse_cover_event_logs(to_block)
  parse_claim_event_logs(to_block)
  parse_verdict_event_logs(to_block)
  parse_vote_event_logs(to_block)
  parse_mcr_event_logs(to_block)
  parse_staking_reward_event_logs(to_block)
  parse_nxm_event_logs(to_block)

  parse_staking_transactions(to_block)
  from_block = get_latest_block_number(Stake) + 1
  parse_stake_event_logs(from_block, to_block)
  parse_unstake_event_logs(from_block, to_block)

  start_block = get_latest_block_number(Transaction) + 1
  parse_eth_transactions(start_block, to_block)
  parse_dai_transactions(start_block, to_block)

  db.session.commit()

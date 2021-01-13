from .. import db, r
from .models import HistoricalPrice
from datetime import datetime
from web3 import Web3
import json
import os
import requests

def query_table(table, order=None):
  rows = []
  query = table.query.all() if order is None else table.query.order_by(order.asc()).all()
  for row in query:
    row = row.__dict__
    del row['_sa_instance_state']
    rows.append(row)
  return rows

def get_last_id(table):
  id = db.session.query(db.func.max(table.id)).scalar()
  return 0 if not id else id

def get_latest_block_number(table):
  if table is None:
    return 0
  block_number = db.session.query(db.func.max(table.block_number)).scalar()
  return 0 if not block_number else block_number

def set_defi_tvl():
  url = 'https://data-api.defipulse.com/api/v1/defipulse/api/GetHistory?api-key=%s' % \
      os.environ['DEFIPULSE_API_KEY']
  tvl = requests.get(url).json()
  tvl_defi = {}
  for date in tvl:
    tvl_defi[str(datetime.utcfromtimestamp(int(date['timestamp'])).date())] = date['tvlUSD']
  r.set('defi_tvl', json.dumps(tvl_defi))

def get_current_mcr_percentage():
  w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/%s' % os.environ['INFURA_PROJECT_ID']))
  with open('abi/mcr.json') as file:
    abi = json.load(file)
  contract = w3.eth.contract(address='0x2EC5d566bd104e01790B13DE33fD51876d57C495', abi=abi)
  mcr = contract.functions.calVtpAndMCRtp().call()[1] / 100
  return mcr

def get_historical_crypto_prices():
  historical_crypto_prices = {}
  for crypto_price in db.session.query(HistoricalPrice):
    historical_crypto_prices[crypto_price.timestamp] = {
      'ETH': crypto_price.eth_price,
      'DAI': crypto_price.dai_price
    }
  return historical_crypto_prices

def add_historical_crypto_price(timestamp):
  if type(timestamp) is str:
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
  crypto_price = db.session.query(HistoricalPrice).filter_by(timestamp=timestamp).first()
  if crypto_price is not None:
    return (crypto_price.eth_price, crypto_price.dai_price)

  api = 'histominute' if (datetime.now() - timestamp).days < 7 else 'histohour'
  url = 'https://min-api.cryptocompare.com/data/%s?fsym=ETH&tsym=USD&limit=1&toTs=%s&api_key=%s' % \
      (api, timestamp.timestamp(), os.environ['CRYPTOCOMPARE_API_KEY'])
  eth_price = requests.get(url).json()['Data'][-1]['close']
  url = 'https://min-api.cryptocompare.com/data/%s?fsym=DAI&tsym=USDT&limit=1&toTs=%s&api_key=%s' % \
      (api, timestamp.timestamp(), os.environ['CRYPTOCOMPARE_API_KEY'])
  dai_price = requests.get(url).json()['Data'][-1]['close']

  db.session.add(HistoricalPrice(
    timestamp=timestamp,
    eth_price=eth_price,
    dai_price=dai_price
  ))
  db.session.commit()
  return (eth_price, dai_price)

def set_current_crypto_prices():
  url = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,DAI&tsyms=USD&api_key=%s' % \
      os.environ['CRYPTOCOMPARE_API_KEY']
  result = requests.get(url).json()
  r.set('ETH', result['ETH']['USD'])
  r.set('DAI', result['DAI']['USD'])

def json_to_csv(graph):
  data = json.loads(r.get(graph))
  if type(data) is list:
    csv = [list(data[0].keys())]
    for row in data:
      csv.append([row[key] for key in csv[0]])
    return csv
  elif 'USD' in data:
    csv = [[''] + list(data.keys())]
    for key in sorted(list(data[csv[0][1]].keys())):
      csv.append([key, data[csv[0][1]][key], data[csv[0][2]][key]])
    return csv
  else:
    csv = []
    for key in sorted(data.keys()):
      csv.append([key, data[key]])
    return csv

def timestamp_to_mcr(mcrs, timestamp):
  if type(timestamp) is str:
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

  low = 0
  high = len(mcrs) - 1
  while low <= high:
    mid = (low + high) // 2
    if mcrs[mid]['timestamp'] < timestamp:
      low = mid + 1
    elif mcrs[mid]['timestamp'] > timestamp:
      high = mid - 1
    else:
      return mcrs[mid]['mcr']

  index = abs(-(low + 1)) - 2
  return 7000 if index < 0 else mcrs[index]['mcr']

def address_to_project(address):
  if not address.startswith('0x'):
    address = '0x' + address
  projects = requests.get('https://api.nexusmutual.io/coverables/contracts.json').json()
  projects = dict((k.lower(), v) for k, v in projects.items())
  if address.lower() in projects:
    return projects[address.lower()]['name']
  return 'Unknown'

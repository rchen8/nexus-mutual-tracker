from datetime import datetime
from dotenv import load_dotenv
import json
import oauth2
import os
import redis
import requests
import sys
import urllib.parse

load_dotenv()

def tweet(status):
  url = 'https://api.twitter.com/1.1/statuses/update.json?status=' + urllib.parse.quote_plus(status)
  consumer = oauth2.Consumer(key=os.environ['CONSUMER_KEY'], secret=os.environ['CONSUMER_SECRET'])
  token = oauth2.Token(key=os.environ['ACCESS_TOKEN'], secret=os.environ['TOKEN_SECRET'])
  response, content = oauth2.Client(consumer, token).request(url, method='POST')

def block_number_to_timestamp(block_number):
  url = 'https://api.etherscan.io/api?module=block&action=getblockreward&blockno=%s&apikey=%s' \
      % (block_number, os.environ['ETHERSCAN_API_KEY'])
  return datetime.fromtimestamp(int(json.loads(requests.get(url).text)['result']['timeStamp']))

def get_latest_block_number():
  url = 'https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=' + \
      os.environ['ETHERSCAN_API_KEY']
  return int(json.loads(requests.get(url).text)['result'], 16) - 2

def get_new_covers(latest_block_number):
  if r.get('last_cover_block_number') is None:
    r.set('last_cover_block_number', latest_block_number)

  last_cover_block_number = int(r.get('last_cover_block_number'))
  for cover in json.loads(requests.get('https://nexustracker.io/all_covers').text):
    if cover['block_number'] > int(r.get('last_cover_block_number')):
      status = \
"""New Cover Purchased!

💳 Cover ID: %s
💼 Project: %s
💲 Cover Amount (USD): $%s
💱 Cover Amount (ETH/DAI): %s %s
💰 Premium: $%s
🕓 Start Date: %s
⏰ Expiration Date: %s

More info: nexustracker.io""" % \
      (
        cover['cover_id'],
        cover['project'],
        str.format('{0:,.2f}', cover['amount_usd']),
        str.format('{:,}', cover['amount']), cover['currency'],
        str.format('{0:,.2f}', cover['premium_usd']),
        cover['start_time'][0:10],
        cover['end_time'][0:10]
      )

      print(status)
      tweet(status)
      last_cover_block_number = max(last_cover_block_number, cover['block_number'])

  r.set('last_cover_block_number', last_cover_block_number)

def get_new_claims(latest_block_number):
  if r.get('last_claim_block_number') is None:
    r.set('last_claim_block_number', latest_block_number)

  last_claim_block_number = int(r.get('last_claim_block_number'))
  for claim in json.loads(requests.get('https://nexustracker.io/all_claims').text):
    if claim['block_number'] > int(r.get('last_claim_block_number')):
      status = \
"""🚨 New Claim Submitted! 🚨

🎫 Claim ID: %s
💳 Cover ID: %s
💼 Project: %s
💲 Claim Amount (USD): $%s
💰 Claim Amount (ETH/DAI): %s %s
🕓 Purchase Date: %s
⏰ Claim Submitted: %s

More info: nexustracker.io/claims""" % \
      (
        claim['claim_id'],
        claim['cover_id'],
        claim['project'],
        str.format('{0:,.2f}', claim['amount_usd']),
        str.format('{:,}', claim['amount']),
        claim['currency'],
        claim['start_time'][0:10],
        claim['timestamp'][0:10]
      )

      print(status)
      tweet(status)
      last_claim_block_number = max(last_claim_block_number, claim['block_number'])

  r.set('last_claim_block_number', last_claim_block_number)

####################################################################################################

if '--heroku' in sys.argv:
  r = redis.from_url(os.environ['REDIS_URL'])
else:
  r = redis.Redis(host='localhost', port=6379)
  
latest_block_number = get_latest_block_number()
get_new_covers(latest_block_number)
get_new_claims(latest_block_number)

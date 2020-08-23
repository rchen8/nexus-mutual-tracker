from app import db
from app.models import *
import sys

if '--daily' in sys.argv:
  utils.set_defi_tvl()
else:
  utils.set_current_crypto_prices()
  parser.parse_etherscan_data()
  grapher.cache_graph_data()

# Nexus Mutual Tracker

## Installation
Get an [Etherscan](https://etherscan.io/apis) and [CoinMarketCap](https://coinmarketcap.com/api/) API key.
```
export ETHERSCAN_API_KEY=<your-etherscan-api-key>
export CMC_API_KEY=<your-cmc-api-key>
pip install -r requirements.txt
sqlite3 app/models/database/nexus.db < app/models/database/create.sql
python server.py
```

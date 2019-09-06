# Nexus Mutual Tracker

## Installation
Get an [Etherscan](https://etherscan.io/apis) and [CoinMarketCap](https://coinmarketcap.com/api/) API key.
```
export ETHERSCAN_API_KEY=<your-etherscan-api-key>
export CMC_API_KEY=<your-cmc-api-key>
pip install -r requirements.txt
```
Create and start a Postgres database named `nexus`. Then run:
```
python
>>> from app import db
>>> db.create_all()
>>> exit()
```
To start the app:
```
python server.py
```

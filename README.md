# Nexus Mutual Tracker

## Installation
Get an [Etherscan](https://etherscan.io/apis) and [DeFi Pulse](https://docs.defipulse.com/) API key. Then run:
```
export ETHERSCAN_API_KEY=<your-etherscan-api-key>
export DEFIPULSE_API_KEY=<your-defipulse-api-key>
brew install redis
pip install -r requirements.txt
```
Create and start a Postgres database named `nexus`. Then run:
```
python -
>>> from app import db
>>> db.create_all()
```
To start the app:
```
python job.py --daily # get DeFi Pulse data
python job.py # populate the database and cache graphs
python server.py # start the app
```

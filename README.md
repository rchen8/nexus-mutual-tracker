# Nexus Mutual Tracker

## Installation
Get a CryptoCompare, DeFi Pulse, Etherscan, Infura, and Twitter API key.
```
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
python job.py # populate the database and cache graphs (will take a while)
python server.py # start the app
```

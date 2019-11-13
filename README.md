# Nexus Mutual Tracker

## Installation
Get an [Etherscan](https://etherscan.io/apis) API key. Then run:
```
export ETHERSCAN_API_KEY=<your-etherscan-api-key>
brew install redis
pip install -r requirements.txt
```
Create and start a Postgres database named `nexus`. Then run:
```
python -
>>> from app import db
>>> db.create_all()
```
If starting the app for the first time, first run `python job.py`. To start the app:
```
python server.py
```

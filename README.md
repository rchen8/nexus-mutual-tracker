# Nexus Mutual Tracker

## Installation
```
export ETHERSCAN_API_KEY=<your-etherscan-api-key>
export DEFIPULSE_API_KEY=<your-defipulse-api-key>
export INFURA_PROJECT_ID=<your-infura-project-id>
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

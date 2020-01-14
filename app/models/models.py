from .. import db

class Cover(db.Model):
  block_number = db.Column(db.Integer, index=True, nullable=False)
  cover_id = db.Column(db.Integer, primary_key=True)
  contract_name = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  premium = db.Column(db.Float, nullable=False)
  currency = db.Column(db.String, nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, index=True, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)
  from_address = db.Column(db.String, nullable=False)
  to_address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  currency = db.Column(db.String, nullable=False)

class StakingTransaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, index=True, nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)
  contract_name = db.Column(db.String, nullable=False)
  address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class StakingReward(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False)
  timestamp = db.Column(db.DateTime, index=True, nullable=False)
  staker = db.Column(db.String, nullable=False)
  contract_name = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class NXMTransaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, index=True, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)
  from_address = db.Column(db.String, nullable=False)
  to_address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class HistoricalPrice(db.Model):
  timestamp = db.Column(db.DateTime, primary_key=True, index=True)
  eth_price = db.Column(db.Float)
  dai_price = db.Column(db.Float)

class MinimumCapitalRequirement(db.Model):
  timestamp = db.Column(db.DateTime, primary_key=True, index=True)
  block_number = db.Column(db.Integer, nullable=False)
  mcr = db.Column(db.Float, nullable=False)

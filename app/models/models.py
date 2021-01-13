from .. import db

class Cover(db.Model):
  block_number = db.Column(db.Integer, nullable=False, index=True)
  cover_id = db.Column(db.Integer, primary_key=True)
  project = db.Column(db.String, nullable=False)
  address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  premium = db.Column(db.Float, nullable=False)
  currency = db.Column(db.String, nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False, index=True)

class Claim(db.Model):
  block_number = db.Column(db.Integer, nullable=False, index=True)
  claim_id = db.Column(db.Integer, primary_key=True)
  cover_id = db.Column(db.Integer, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)
  verdict = db.Column(db.String, default='Pending')

class Vote(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False, index=True)
  claim_id = db.Column(db.Integer, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  timestamp = db.Column(db.DateTime, nullable=False)
  verdict = db.Column(db.String, nullable=False)

class Stake(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False, index=True)
  timestamp = db.Column(db.DateTime, nullable=False)
  staker = db.Column(db.String, nullable=False)
  project = db.Column(db.String, nullable=False)
  address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class StakingReward(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False, index=True)
  timestamp = db.Column(db.DateTime, nullable=False)
  project = db.Column(db.String, nullable=False)
  address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False, index=True)
  timestamp = db.Column(db.DateTime, nullable=False)
  from_address = db.Column(db.String, nullable=False)
  to_address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)
  currency = db.Column(db.String, nullable=False)

class NXMTransaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False, index=True)
  timestamp = db.Column(db.DateTime, nullable=False)
  from_address = db.Column(db.String, nullable=False)
  to_address = db.Column(db.String, nullable=False)
  amount = db.Column(db.Float, nullable=False)

class HistoricalPrice(db.Model):
  timestamp = db.Column(db.DateTime, primary_key=True)
  eth_price = db.Column(db.Float, nullable=False)
  dai_price = db.Column(db.Float, nullable=False)

class MinimumCapitalRequirement(db.Model):
  timestamp = db.Column(db.DateTime, primary_key=True)
  block_number = db.Column(db.Integer, nullable=False)
  mcr = db.Column(db.Float, nullable=False)

CREATE TABLE IF NOT EXISTS Covers(
  block_number NUMERIC NOT NULL,
  cover_id NUMERIC NOT NULL,
  contract_name TEXT NOT NULL,
  amount NUMERIC NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Transactions(
  block_number NUMERIC NOT NULL,
  _timestamp DATETIME NOT NULL,
  from_address TEXT NOT NULL,
  to_address TEXT NOT NULL,
  amount NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS StakingTransactions(
  block_number NUMERIC NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  contract_name TEXT NOT NULL,
  amount NUMERIC NOT NULL
);

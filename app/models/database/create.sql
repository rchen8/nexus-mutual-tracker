CREATE TABLE Covers(
  id NUMERIC NOT NULL,
  contract_name TEXT NOT NULL,
  amount NUMERIC NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL
);

CREATE TABLE Transactions(
  _timestamp DATETIME NOT NULL,
  from_address TEXT NOT NULL,
  to_address TEXT NOT NULL,
  amount NUMERIC NOT NULL
);

CREATE TABLE StakingTransactions(
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  contract_name TEXT NOT NULL,
  amount NUMERIC NOT NULL
);

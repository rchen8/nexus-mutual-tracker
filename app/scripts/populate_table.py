# Run this in the root directory of the app

from app import db
from app.models.models import NXMTransaction
import csv

with open('nxm_transaction.csv') as file:
  reader = csv.reader(file)
  for row in reader:
    print(row)
    db.session.add(NXMTransaction(
      id=row[0],
      block_number=row[1],
      timestamp=row[2],
      from_address=row[3],
      to_address=row[4],
      amount=float(row[5])
    ))
    db.session.commit()

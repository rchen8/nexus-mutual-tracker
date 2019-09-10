# Run this in the root directory of the app

from app import db
from app.models.models import HistoricalPrice
import csv

with open('historical_price.csv') as file:
  reader = csv.reader(file)
  for row in reader:
    print(row)
    db.session.add(HistoricalPrice(
      timestamp=row[0],
      eth_price=float(row[1]),
      dai_price=float(row[2])
    ))
    db.session.commit()

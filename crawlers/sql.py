# In this module we will put all raw SQL queries which have to do with crawling app

INSERT_STOCKS = """\
INSERT INTO crawlers_stockhistory (currency, price, market_cap, timestamp)
VALUES
    %s
ON CONFLICT ON CONSTRAINT unique_timestamp_currency
DO 
   UPDATE SET price = EXCLUDED.price
"""

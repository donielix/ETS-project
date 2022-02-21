PCT_CHANGE = """\
SELECT
    currency,
    price,
    timestamp,
    price / NULLIF(prev_price, 0) - 1 AS pct_change
    FROM (
    SELECT 
        currency,
        price,
        timestamp,
        lag(price, 1) OVER (PARTITION BY currency ORDER BY timestamp ASC) AS prev_price
    FROM crawlers_stockhistory
    ORDER BY currency, timestamp
    ) t1
"""

UPDATE_PCT_CHANGE = """\
WITH subquery AS (
    SELECT
        id,
        price,
        price / NULLIF(prev_price, 0) - 1 AS pct_change
        FROM (
        SELECT
            id,
            price,
            lag(price, 1) OVER (PARTITION BY currency ORDER BY timestamp ASC) AS prev_price
        FROM crawlers_stockhistory
        WHERE date(timestamp) BETWEEN %(from_date)s AND %(date)s
        ) t1
)
UPDATE crawlers_stockhistory
SET pct_change = subquery.pct_change
FROM subquery
WHERE crawlers_stockhistory.id = subquery.id
"""

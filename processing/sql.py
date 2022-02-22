

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

# An aggregate function must be previously created with
# CREATE AGGREGATE cumulative_mul(float8) (SFUNC = float8mul, STYPE = float8)
CALCULATE_INDEX = """\
WITH x AS (
    SELECT
        date(timestamp) AS date,
        SUM(pct_change) + 1 AS return_sum
    FROM
        crawlers_stockhistory
    WHERE currency in %(commodities)s
    AND date(timestamp) <= %(date)s
    GROUP BY date(timestamp)
    ORDER BY date(timestamp)
)

SELECT
    100 * cumulative_mul(return_sum) OVER (ORDER BY date) AS price_index
FROM x
WHERE date = %(date)s
"""

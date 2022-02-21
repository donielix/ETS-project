import jsonutils as js
import pandas as pd
import requests
from celery import chain, group, shared_task
from django.db import connection
from processing.tasks import calculate_pct_change

from crawlers.sql import INSERT_STOCKS


@shared_task
def crawl_coin_date(date, convert="USD,EUR", limit=5000):
    """
    Crawls a single date from historical coin's market API, and save it to database with a bulk insert.

    Params
    ------
        date: str: Target date, in any format that json-enhanced can understand.
        convert: str: Show value in terms of the current value of the selected currencies.
        limit: int: An external REST API param.
    """

    # parse user input date to an ISO date format
    date = js.parse_datetime(date).date().strftime("%Y-%m-%d")
    BASE_URL = "https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical"
    REQUEST_PARAMS = {"convert": convert, "date": date, "limit": limit}

    # make a GET request to external API and store response as JSON object.
    response = requests.get(BASE_URL, params=REQUEST_PARAMS).json()

    coin_list = response["data"]
    # ==== Response example (single instance) ====
    # {
    #     "id": 2245,
    #     "name": "Presearch",
    #     "symbol": "PRE",
    #     "slug": "presearch",
    #     "num_market_pairs": 6,
    #     "date_added": "2017-12-05T00:00:00.000Z",
    #     "tags": ["platform", "crowdsourcing", "search-engine"],
    #     "max_supply": 500000000,
    #     "circulating_supply": 172742423.99999997,
    #     "total_supply": 500000000,
    #     "platform": {
    #         "id": 1027,
    #         "name": "Ethereum",
    #         "symbol": "ETH",
    #         "slug": "ethereum",
    #         "token_address": "0xEC213F83defB583af3A000B1c0ada660b1902A0F",
    #     },
    #     "cmc_rank": 1000,
    #     "self_reported_circulating_supply": None,
    #     "self_reported_market_cap": None,
    #     "last_updated": "2021-01-01T23:00:00.000Z",
    #     "quote": {
    #         "EUR": {
    #             "price": 0.011638380113624353,
    #             "volume_24h": 53460.01357141365,
    #             "percent_change_1h": 0.083401175932,
    #             "percent_change_24h": 1.204507120947,
    #             "percent_change_7d": -7.719049146918,
    #             "market_cap": 2010441.9922608659,
    #             "fully_diluted_market_cap": None,
    #             "last_updated": "2021-01-01T23:59:06.000Z",
    #         }
    #     },
    # }

    # retrieve a list of values to insert in BBDD as a SQL command
    values = [
        (
            c["slug"],
            c["quote"]["EUR"]["price"],
            c["quote"]["EUR"]["market_cap"],
            c["quote"]["EUR"]["last_updated"],
        )
        for c in coin_list
    ]

    # format values in a right way
    values = ", ".join(map(str, values))

    # make SQL insert into database
    with connection.cursor() as cursor:
        cursor.execute(INSERT_STOCKS % values)


@shared_task
def crawl_coin_period(start_date, end_date, freq="D", **kwargs):
    """
    Crawls a range period, from `start_date` to `end_date`, and frequency `freq`. This is executed as a batch process.
    """

    date_range = (
        pd.date_range(start_date, end_date, freq=freq).strftime("%Y-%m-%d").tolist()
    )

    # concurrently call to crawl_coint_date function
    group(crawl_coin_date.s(date, **kwargs) for date in date_range)()


@shared_task
def start_jobs(date):
    """
    Execute the main flow, consisting on a chain of tasks. This must be called as a streaming process
    """

    chain(crawl_coin_date.si(date), calculate_pct_change.si(date))()

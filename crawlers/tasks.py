import jsonutils as js
import pandas as pd
import requests
from celery import group, shared_task
from django.db import connection

from crawlers.sql import INSERT_STOCKS


@shared_task
def crawl_coin_date(date, convert="USD,BTC,EUR", limit=5000):
    """
    Crawls a single date from historical coin's market API, and save it to database.

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

    values = [
        (
            c["slug"],
            c["quote"]["EUR"]["price"],
            c["quote"]["EUR"]["market_cap"],
            c["quote"]["EUR"]["last_updated"],
        )
        for c in coin_list
    ]

    values = ", ".join(map(str, values))

    with connection.cursor() as cursor:
        cursor.execute(INSERT_STOCKS % values)


@shared_task
def crawl_coin_period(start_date, end_date, **kwargs):
    """
    :type period: tuple
    """

    date_range = (
        pd.date_range(start_date, end_date, freq="D").strftime("%Y-%m-%d").tolist()
    )

    group(crawl_coin_date.s(date, **kwargs) for date in date_range)()

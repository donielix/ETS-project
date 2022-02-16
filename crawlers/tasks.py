import os

import jsonutils as js
import pandas as pd
from celery import group, shared_task

from crawlers.serializers import StockHistorySerializer


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

    # parse input date to an ISO date format
    date = js.parse_datetime(date).date().strftime("%Y-%m-%d")
    BASE_URL = "https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical"
    REQUEST_PARAMS = {"convert": convert, "date": date, "limit": limit}

    # with json-enhanced, make a GET request to external API and store response as a queryable JSON object.
    response = js.JSONObject.open(BASE_URL, params=REQUEST_PARAMS)

    queryset = response.query(market_cap=js.All).values(
        "market_cap",
        "price",
        "num_market_pairs",
        "total_supply",
        "max_supply",
        "cmc_rank",
        "symbol",
        currency="name",
    )

    stock_serializer = StockHistorySerializer(data=queryset, many=True)
    stock_serializer.is_valid(raise_exception=True)
    stock_serializer.save()

    return response._data


@shared_task
def crawl_coin_period(start_date, end_date, **kwargs):
    """
    :type period: tuple
    """

    date_range = (
        pd.date_range(start_date, end_date, freq="D").strftime("%Y-%m-%d").tolist()
    )

    group(crawl_coin_date.s(date, **kwargs) for date in date_range)()

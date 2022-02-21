from datetime import timedelta

import jsonutils as js
from celery import shared_task
from django.db import connection

from processing.sql import UPDATE_PCT_CHANGE


@shared_task
def calculate_pct_change(date, days_lag=2):
    date = js.parse_datetime(date).date()
    from_date = date - timedelta(days=days_lag)
    with connection.cursor() as cursor:
        cursor.execute(UPDATE_PCT_CHANGE, params={"date": date, "from_date": from_date})

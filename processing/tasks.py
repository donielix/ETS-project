from celery import shared_task
from django.db import connection

from processing.sql import UPDATE_PCT_CHANGE


@shared_task
def calculate_pct_change():
    with connection.cursor() as cursor:
        cursor.execute(UPDATE_PCT_CHANGE)

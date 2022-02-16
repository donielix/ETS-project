from django.db import models


class StockHistory(models.Model):
    currency = models.CharField(max_length=100, help_text="Name of the currency")
    symbol = models.CharField(max_length=50, help_text="Symbol of the currency")
    cmc_rank = models.IntegerField(null=True, blank=True)
    max_supply = models.FloatField(null=True, blank=True)
    total_supply = models.FloatField(null=True, blank=True)
    num_market_pairs = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

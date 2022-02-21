from django.db import models


class StockHistory(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["currency", "timestamp"], name="unique_timestamp_currency"
            ),
        ]
        ordering = ["currency", "timestamp"]

    currency = models.CharField(max_length=100, help_text="Name of the currency")
    price = models.FloatField()
    market_cap = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()
    pct_change = models.FloatField(null=True, blank=True)

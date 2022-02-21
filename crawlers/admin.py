from django.contrib import admin

from .models import StockHistory


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "currency",
        "price",
        "market_cap",
        "timestamp",
        "pct_change",
    )
    list_filter = ("timestamp",)

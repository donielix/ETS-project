from graphene_django import DjangoObjectType
from crawlers.models import StockHistory
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from django.db import connection
from processing.sql import CALCULATE_INDEX


class PriceIndexType(graphene.ObjectType):
    price_index = graphene.Float()


class StockHistoryNode(DjangoObjectType):
    class Meta:
        model = StockHistory
        filter_fields = {
            "currency": ["exact", "in", "contains"],
            "timestamp": ["exact", "gt", "gte", "lt", "lte", "range"],
            "pct_change": ["gt", "gte", "lt", "lte", "range"],
        }
        fields = "__all__"
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):

    all_stocks = DjangoFilterConnectionField(StockHistoryNode)
    price_index = graphene.Field(
        PriceIndexType,
        date=graphene.Date(required=True),
        commodities=graphene.List(graphene.String, required=True),
    )

    def resolve_all_stocks(root, info, **kwargs):
        return StockHistory.objects.all().order_by("currency", "timestamp")

    def resolve_price_index(root, info, date, commodities):

        with connection.cursor() as cursor:
            cursor.execute(
                CALCULATE_INDEX,
                params={"commodities": tuple(commodities), "date": date},
            )
            res = cursor.fetchone()

        return PriceIndexType(price_index=res[0])

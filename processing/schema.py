from graphene_django import DjangoObjectType
from crawlers.models import StockHistory
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField


class StockHistoryNode(DjangoObjectType):
    class Meta:
        model = StockHistory
        filter_fields = {
            "currency": ["exact", "in"],
            "timestamp": ["exact", "gt", "gte", "lt", "lte", "range"],
        }
        fields = "__all__"
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):

    all_stocks = DjangoFilterConnectionField(StockHistoryNode)

    def resolve_all_stocks(root, info, **kwargs):
        return StockHistory.objects.all()

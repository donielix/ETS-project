from graphene_django import DjangoObjectType
from crawlers.models import StockHistory
import graphene

class StockHistoryType(DjangoObjectType):
    class Meta:
        model = StockHistory
        fields = "__all__"

class Query(graphene.ObjectType):

    all_stocks = graphene.List(StockHistoryType)

    def resolve_all_stocks(root, info):
        return StockHistory.objects.all()
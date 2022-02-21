import graphene
from processing.schema import Query as processingQuery

class Query(processingQuery):
    pass

schema = graphene.Schema(query=Query)
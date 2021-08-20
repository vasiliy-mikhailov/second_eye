from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class FunctionComponentKindType(DjangoObjectType):
    class Meta:
        model = FunctionComponentKind
        fields = "__all__"
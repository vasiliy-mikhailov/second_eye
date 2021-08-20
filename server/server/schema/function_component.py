from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class FunctionComponentType(DjangoObjectType):
    class Meta:
        model = FunctionComponent
        fields = "__all__"
from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class SystemType(DjangoObjectType):
    class Meta:
        model = System
        fields = "__all__"
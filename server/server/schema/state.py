from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class StateType(DjangoObjectType):
    class Meta:
        model = State
        fields = "__all__"



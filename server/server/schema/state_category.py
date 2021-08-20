from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class StateCategoryType(DjangoObjectType):
    class Meta:
        model = StateCategory
        fields = "__all__"
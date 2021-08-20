from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = "__all__"
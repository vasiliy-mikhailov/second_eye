import graphene
from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        fields = "__all__"
import graphene
from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *


class ChangeRequestTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = ChangeRequestTimeSheetsByDate
        fields = "__all__"


class ChangeRequestAnalysisTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = ChangeRequestAnalysisTimeSheetsByDate
        fields = "__all__"


class ChangeRequestDevelopmentTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = ChangeRequestDevelopmentTimeSheetsByDate
        fields = "__all__"


class ChangeRequestTestingTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = ChangeRequestTestingTimeSheetsByDate
        fields = "__all__"


class ChangeRequestType(DjangoObjectType):
    state_category_id = graphene.Int()

    class Meta:
        model = ChangeRequest
        fields = "__all__"
from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class SystemChangeRequestTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequestTimeSheetsByDate
        fields = "__all__"


class SystemChangeRequestAnalysisTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequestAnalysisTimeSheetsByDate
        fields = "__all__"


class SystemChangeRequestDevelopmentTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequestDevelopmentTimeSheetsByDate
        fields = "__all__"


class SystemChangeRequestTestingTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequestTestingTimeSheetsByDate
        fields = "__all__"


class SystemChangeRequestType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequest
        fields = "__all__"
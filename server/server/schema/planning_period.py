from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class PlanningPeriodType(DjangoObjectType):
    class Meta:
        model = PlanningPeriod
        fields = "__all__"


class PlanningPeriodTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = PlanningPeriodTimeSheetsByDate
        fields = "__all__"


class PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateType(DjangoObjectType):
    class Meta:
        model = PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
        fields = "__all__"
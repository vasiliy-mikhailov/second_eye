from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class DedicatedTeamType(DjangoObjectType):
    class Meta:
        model = DedicatedTeam
        fields = "__all__"


class DedicatedTeamPositionType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPosition
        fields = "__all__"


class DedicatedTeamPositionAbilityType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPositionAbility
        fields = "__all__"


class DedicatedTeamPlanningPeriodType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPlanningPeriod
        fields = "__all__"


class DedicatedTeamPlanningPeriodTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPlanningPeriodTimeSheetsByDate
        fields = "__all__"


class DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
        fields = "__all__"
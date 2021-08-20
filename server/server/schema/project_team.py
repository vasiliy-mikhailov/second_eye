from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class ProjectTeamType(DjangoObjectType):
    class Meta:
        model = ProjectTeam
        fields = "__all__"


class ProjectTeamPlanningPeriodType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPlanningPeriod
        fields = "__all__"


class ProjectTeamPlanningPeriodTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPlanningPeriodTimeSheetsByDate
        fields = "__all__"


class ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
        fields = "__all__"


class ProjectTeamPositionAbilityType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPositionAbility
        fields = "__all__"


class ProjectTeamPositionType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPosition
        fields = "__all__"
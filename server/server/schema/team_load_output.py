import graphene
from graphene_django import DjangoObjectType
from second_eye_api.models.team_load_output import *

class TeamLoadOutputPlanningPeriodType(DjangoObjectType):
    class Meta:
        model = TeamLoadOutputPlanningPeriod
        fields = "__all__"

class TeamLoadOutputDedicatedTeamType(DjangoObjectType):
    class Meta:
        model = TeamLoadOutputDedicatedTeam
        fields = "__all__"

class TeamLoadOutputSkillType(DjangoObjectType):
    class Meta:
        model = TeamLoadOutputSkill
        fields = "__all__"

class TeamLoadOutputSystemType(DjangoObjectType):
    class Meta:
        model = TeamLoadOutputSystem
        fields = "__all__"

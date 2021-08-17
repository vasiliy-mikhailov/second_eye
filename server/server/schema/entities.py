import graphene
from graphene_django import DjangoObjectType
from second_eye_api.models.entities import *

class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = "__all__"

class SystemType(DjangoObjectType):
    class Meta:
        model = System
        fields = "__all__"

class StateType(DjangoObjectType):
    class Meta:
        model = State
        fields = "__all__"

class StateCategoryType(DjangoObjectType):
    class Meta:
        model = StateCategory
        fields = "__all__"

class DedicatedTeamType(DjangoObjectType):
    class Meta:
        model = DedicatedTeam
        fields = "__all__"

class ProjectTeamType(DjangoObjectType):
    class Meta:
        model = ProjectTeam
        fields = "__all__"

class ChangeRequestType(DjangoObjectType):
    state_id = graphene.Int()

    class Meta:
        model = ChangeRequest
        fields = "__all__"

class SystemChangeRequestType(DjangoObjectType):
    class Meta:
        model = SystemChangeRequest
        fields = "__all__"

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"

class FunctionComponentType(DjangoObjectType):
    class Meta:
        model = FunctionComponent
        fields = "__all__"

class FunctionComponentKindType(DjangoObjectType):
    class Meta:
        model = FunctionComponentKind
        fields = "__all__"

class DedicatedTeamPositionType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPosition
        fields = "__all__"

class ProjectTeamPositionType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPosition
        fields = "__all__"

class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = "__all__"

class DedicatedTeamPositionAbilityType(DjangoObjectType):
    class Meta:
        model = DedicatedTeamPositionAbility
        fields = "__all__"

class ProjectTeamPositionAbilityType(DjangoObjectType):
    class Meta:
        model = ProjectTeamPositionAbility
        fields = "__all__"

class TaskTimeSheetsType(DjangoObjectType):
    class Meta:
        model = TaskTimeSheets
        fields = "__all__"

class PlanningPeriodType(DjangoObjectType):
    class Meta:
        model = PlanningPeriod
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

class TaskTimeSheetsByDateType(DjangoObjectType):
    class Meta:
        model = TaskTimeSheetsByDate
        fields = "__all__"

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

import graphene
from graphene_django import DjangoObjectType

from second_eye_api.models import *

class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = "__all__"

class SystemType(DjangoObjectType):
    class Meta:
        model = System
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

class Query(graphene.ObjectType):
    all_dedicated_teams = graphene.List(DedicatedTeamType)
    all_project_teams = graphene.List(ProjectTeamType)
    all_skills = graphene.List(SkillType)
    all_tasks = graphene.List(TaskType)

    def resolve_all_dedicated_teams(root, info):
        return DedicatedTeam.objects.all()

    def resolve_all_project_teams(root, info):
        return ProjectTeam.objects.all()

    def resolve_all_skills(root, info):
        return Skill.objects.all()

    def resolve_all_tasks(root, info):
        return Task.objects.all()

schema = graphene.Schema(query=Query)
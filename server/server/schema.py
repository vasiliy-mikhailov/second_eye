import graphene
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer
from graphene_django.debug import DjangoDebug

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

class PersonType(DjangoObjectType):
    class Meta:
        model = Person
        fields = "__all__"

class Query(graphene.ObjectType):
    all_dedicated_teams = graphene.List(DedicatedTeamType)
    all_project_teams = graphene.List(ProjectTeamType)
    all_change_requests = graphene.List(ChangeRequestType)
    all_skills = graphene.List(SkillType)
    all_systems = graphene.List(SystemType)
    all_tasks = graphene.List(TaskType)
    all_persons = graphene.List(PersonType)
    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_all_dedicated_teams(root, info):
        return gql_optimizer.query(DedicatedTeam.objects.all(), info)

    def resolve_all_project_teams(root, info):
        return gql_optimizer.query(ProjectTeam.objects.all(), info)

    def resolve_all_change_requests(root, info):
        return gql_optimizer.query(ChangeRequest.objects.all(), info)

    def resolve_all_skills(root, info):
        return gql_optimizer.query(Skill.objects.all(), info)

    def resolve_all_systems(root, info):
        return gql_optimizer.query(System.objects.all(), info)

    def resolve_all_tasks(root, info):
        return gql_optimizer.query(Task.objects.all(), info)

    def resolve_all_persons(root, info):
        return gql_optimizer.query(Person.objects.all(), info)

schema = graphene.Schema(query=Query)
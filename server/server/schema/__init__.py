import graphene_django_optimizer as gql_optimizer
from graphene_django.debug import DjangoDebug
from .change_request import *
from .dedicated_team import *
from .function_component import *
from .person import *
from .planning_period import *
from .project_team import *
from .skill import *
from .state import *
from .state_category import *
from .system import *
from .system_change_request import *
from .task import *
from .team_load_output import *

class Query(graphene.ObjectType):
    planning_periods = graphene.List(PlanningPeriodType)
    dedicated_teams = graphene.List(DedicatedTeamType)
    project_teams = graphene.List(ProjectTeamType)
    state_categories = graphene.List(StateCategoryType)
    states = graphene.List(StateType)
    change_requests = graphene.List(ChangeRequestType)
    system_change_requests = graphene.List(SystemChangeRequestType)
    skills = graphene.List(SkillType)
    systems = graphene.List(SystemType)
    tasks = graphene.List(TaskType)
    function_components = graphene.List(FunctionComponentType)
    persons = graphene.List(PersonType)
    task_time_sheets = graphene.List(TaskTimeSheetsType)

    dedicated_teams_load = graphene.List(TeamLoadOutputPlanningPeriodType)

    planning_period_by_id = graphene.Field(PlanningPeriodType, id=graphene.String())
    change_request_by_id = graphene.Field(ChangeRequestType, id=graphene.String())
    system_change_request_by_id = graphene.Field(SystemChangeRequestType, id=graphene.String())
    task_by_id = graphene.Field(TaskType, id=graphene.String())

    dedicated_team_planning_periods = graphene.List(DedicatedTeamPlanningPeriodType)

    dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id = graphene.Field(DedicatedTeamPlanningPeriodType, planning_period_id=graphene.String(), dedicated_team_id=graphene.String())
    change_requests_by_planning_period_id_and_dedicated_team_id = graphene.List(ChangeRequestType, planning_period_id=graphene.String(), dedicated_team_id=graphene.String())

    debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_planning_periods(root, info):
        return gql_optimizer.query(PlanningPeriod.objects.all(), info)

    def resolve_dedicated_teams(root, info):
        return gql_optimizer.query(DedicatedTeam.objects.all(), info)

    def resolve_project_teams(root, info):
        return gql_optimizer.query(ProjectTeam.objects.all(), info)

    def resolve_state_categories(root, info):
        return gql_optimizer.query(StateCategory.objects.all(), info)

    def resolve_states(root, info):
        return gql_optimizer.query(State.objects.all(), info)

    def resolve_change_requests(root, info):
        return ChangeRequest.objects.all()

    def resolve_system_change_requests(root, info):
        return SystemChangeRequest.objects.all()

    def resolve_skills(root, info):
        return gql_optimizer.query(Skill.objects.all(), info)

    def resolve_systems(root, info):
        return gql_optimizer.query(System.objects.all(), info)

    def resolve_tasks(root, info):
        return Task.objects.all()

    def resolve_function_components(root, info):
        return gql_optimizer.query(FunctionComponent.objects.all(), info)

    def resolve_persons(root, info):
        return gql_optimizer.query(Person.objects.all(), info)

    def resolve_dedicated_teams_load(root, info):
        return gql_optimizer.query(TeamLoadOutputPlanningPeriod.objects.all(), info)

    def resolve_task_time_sheets(root, info):
        return gql_optimizer.query(TaskTimeSheets.objects.all(), info)

    def resolve_planning_period_by_id(root, info, id):
        return PlanningPeriod.objects.get(pk=id)

    def resolve_change_request_by_id(root, info, id):
        return ChangeRequest.objects.get(pk=id)

    def resolve_system_change_request_by_id(root, info, id):
        return SystemChangeRequest.objects.get(pk=id)

    def resolve_task_by_id(root, info, id):
        return Task.objects.get(pk=id)

    def resolve_dedicated_team_planning_periods(root, info):
        return DedicatedTeamPlanningPeriod.objects.all()

    def resolve_dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
        return DedicatedTeamPlanningPeriod.objects.get(planning_period_id=planning_period_id, dedicated_team_id=dedicated_team_id)

    def resolve_change_requests_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
        return ChangeRequest.objects.filter(planning_period_id=planning_period_id, dedicated_team_id=dedicated_team_id)


schema = graphene.Schema(query=Query)
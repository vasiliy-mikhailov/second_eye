from django.conf import settings
import graphene
import graphene_django_optimizer as gql_optimizer

from second_eye_api.schema.change_request import ChangeRequest
from second_eye_api.schema.company import Company
from second_eye_api.schema.dedicated_team import DedicatedTeam, DedicatedTeamPlanningPeriod
from second_eye_api.schema.planning_period import PlanningPeriod
from second_eye_api.schema.project_team import ProjectTeam, ProjectTeamPlanningPeriod
from second_eye_api.schema.state import State
from second_eye_api.schema.state_category import StateCategory
from second_eye_api.schema.skill import Skill
from second_eye_api.schema.system import System
from second_eye_api.schema.system_change_request import SystemChangeRequest

def get_data_store():
    result = settings.GRAPHENE_FRAME_DATA_STORE
    return result

class Query(graphene.ObjectType):
    planning_periods = graphene.List(PlanningPeriod)
    companies = graphene.List(Company)
    dedicated_teams = graphene.List(DedicatedTeam)
    project_teams = graphene.List(ProjectTeam)
    state_categories = graphene.List(StateCategory)
    states = graphene.List(State)
    change_requests = graphene.List(ChangeRequest)
    system_change_requests = graphene.List(SystemChangeRequest)
    skills = graphene.List(Skill)
    systems = graphene.List(System)
    # tasks = graphene.List(TaskType)
    # function_components = graphene.List(FunctionComponentType)
    # persons = graphene.List(PersonType)
    # task_time_sheets = graphene.List(TaskTimeSheetsType)
    #
    planning_period_by_id = graphene.Field(PlanningPeriod, id=graphene.Int())
    change_request_by_id = graphene.Field(ChangeRequest, id=graphene.String())
    system_change_request_by_id = graphene.Field(SystemChangeRequest, id=graphene.String())
    # task_by_id = graphene.Field(TaskType, id=graphene.String())
    #
    dedicated_team_planning_periods = graphene.List(DedicatedTeamPlanningPeriod)

    dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id = graphene.Field(
        DedicatedTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        dedicated_team_id=graphene.Int()
    )

    project_team_planning_period_by_planning_period_id_and_project_team_id = graphene.Field(
        ProjectTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        project_team_id=graphene.Int()
    )
    #
    # change_requests_by_planning_period_id_and_dedicated_team_id = graphene.List(ChangeRequestType, planning_period_id=graphene.String(), dedicated_team_id=graphene.String())
    #
    # debug = graphene.Field(DjangoDebug, name='_debug')

    def resolve_planning_periods(root, info):
        return PlanningPeriod.all(data_store=get_data_store())

    def resolve_companies(root, info):
        return Company.all(data_store=get_data_store())

    def resolve_dedicated_teams(root, info):
        return DedicatedTeam.all(data_store=get_data_store())
    #
    def resolve_project_teams(root, info):
        return ProjectTeam.all(data_store=get_data_store())
    #
    def resolve_state_categories(root, info):
        return StateCategory.all(data_store=get_data_store())
    #
    def resolve_states(root, info):
        return State.all(data_store=get_data_store())
    #
    def resolve_change_requests(root, info):
        return gql_optimizer.query(ChangeRequest.all(data_store=get_data_store()), info)

    def resolve_system_change_requests(root, info):
        return SystemChangeRequest.all(data_store=get_data_store())

    def resolve_skills(root, info):
        return Skill.all(data_store=get_data_store())
    #
    def resolve_systems(root, info):
        return System.all(data_store=get_data_store())
    #
    # def resolve_tasks(root, info):
    #     return Task.objects.all()
    #
    # def resolve_function_components(root, info):
    #     return gql_optimizer.query(FunctionComponent.objects.all(), info)
    #
    # def resolve_persons(root, info):
    #     return gql_optimizer.query(Person.objects.all(), info)
    #
    # def resolve_dedicated_teams_load(root, info):
    #     return gql_optimizer.query(TeamLoadOutputPlanningPeriod.objects.all(), info)
    #
    # def resolve_task_time_sheets(root, info):
    #     return gql_optimizer.query(TaskTimeSheets.objects.all(), info)
    #
    def resolve_planning_period_by_id(root, info, id):
        return PlanningPeriod.get_by_primary_key_value(value=id, data_store=get_data_store())
    #
    def resolve_change_request_by_id(root, info, id):
        return ChangeRequest.get_by_primary_key_value(value=id, data_store=get_data_store())

    def resolve_system_change_request_by_id(root, info, id):
        return SystemChangeRequest.get_by_primary_key_value(value=id, data_store=get_data_store())
    #
    # def resolve_task_by_id(root, info, id):
    #     return Task.objects.get(pk=id)
    #
    def resolve_dedicated_team_planning_periods(root, info):
        return DedicatedTeamPlanningPeriod.all(data_store=get_data_store())

    def resolve_dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
        return DedicatedTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'dedicated_team_id': dedicated_team_id
        }, data_store=get_data_store())

    def resolve_project_team_planning_period_by_planning_period_id_and_project_team_id(root, info, planning_period_id, project_team_id):
        return ProjectTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'project_team_id': project_team_id
        }, data_store=get_data_store())

    # def resolve_change_requests_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
    #     return ChangeRequest.objects.filter(planning_period_id=planning_period_id, dedicated_team_id=dedicated_team_id)


schema = graphene.Schema(query=Query)
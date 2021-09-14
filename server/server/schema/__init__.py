from django.conf import settings
import graphene
import graphene_django_optimizer as gql_optimizer

from second_eye_api.schema import change_request
from second_eye_api.schema import company
from second_eye_api.schema import dedicated_team
from second_eye_api.schema import person
from second_eye_api.schema import planning_period
from second_eye_api.schema import project_team
from second_eye_api.schema import state
from second_eye_api.schema import state_category
from second_eye_api.schema import skill
from second_eye_api.schema import system
from second_eye_api.schema import system_change_request

def get_data_store():
    result = settings.GRAPHENE_FRAME_DATA_STORE
    return result

class Query(graphene.ObjectType):
    planning_periods = graphene.List(planning_period.PlanningPeriod)
    companies = graphene.List(company.Company)
    dedicated_teams = graphene.List(dedicated_team.DedicatedTeam)
    project_teams = graphene.List(project_team.ProjectTeam)
    state_categories = graphene.List(state_category.StateCategory)
    states = graphene.List(state.State)
    change_requests = graphene.List(change_request.ChangeRequest)
    system_change_requests = graphene.List(system_change_request.SystemChangeRequest)
    skills = graphene.List(skill.Skill)
    systems = graphene.List(system.System)
    persons = graphene.List(person.Person)

    planning_period_by_id = graphene.Field(planning_period.PlanningPeriod, id=graphene.Int())
    change_request_by_id = graphene.Field(change_request.ChangeRequest, id=graphene.String())
    system_change_request_by_id = graphene.Field(system_change_request.SystemChangeRequest, id=graphene.String())

    dedicated_team_planning_periods = graphene.List(dedicated_team.DedicatedTeamPlanningPeriod)

    dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id = graphene.Field(
        dedicated_team.DedicatedTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        dedicated_team_id=graphene.Int()
    )

    project_team_planning_period_by_planning_period_id_and_project_team_id = graphene.Field(
        project_team.ProjectTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        project_team_id=graphene.Int()
    )

    systems = graphene.List(system.System)

    system_planning_periods = graphene.List(system.SystemPlanningPeriod)

    system_planning_period_by_planning_period_id_and_system_id = graphene.Field(
        system.SystemPlanningPeriod,
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )

    project_team_planning_period_system_by_project_team_id_planning_period_id_and_system_id = graphene.Field(
        project_team.ProjectTeamPlanningPeriodSystem,
        project_team_id=graphene.Int(),
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )

    dedicated_team_planning_period_system_by_dedicated_team_id_planning_period_id_and_system_id = graphene.Field(
        dedicated_team.DedicatedTeamPlanningPeriodSystem,
        dedicated_team_id=graphene.Int(),
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )

    def resolve_planning_periods(root, info):
        return planning_period.PlanningPeriod.all(data_store=get_data_store())

    def resolve_companies(root, info):
        return company.Company.all(data_store=get_data_store())

    def resolve_dedicated_teams(root, info):
        return dedicated_team.DedicatedTeam.all(data_store=get_data_store())

    def resolve_project_teams(root, info):
        return project_team.ProjectTeam.all(data_store=get_data_store())

    def resolve_state_categories(root, info):
        return state_category.StateCategory.all(data_store=get_data_store())

    def resolve_states(root, info):
        return state.State.all(data_store=get_data_store())

    def resolve_change_requests(root, info):
        return gql_optimizer.query(ChangeRequest.all(data_store=get_data_store()), info)

    def resolve_system_change_requests(root, info):
        return system_change_request.SystemChangeRequest.all(data_store=get_data_store())

    def resolve_skills(root, info):
        return skill.Skill.all(data_store=get_data_store())

    def resolve_systems(root, info):
        return system.System.all(data_store=get_data_store())

    def resolve_persons(root, info):
        return person.Person.all(data_store=get_data_store())

    def resolve_planning_period_by_id(root, info, id):
        return planning_period.PlanningPeriod.get_by_primary_key_value(value=id, data_store=get_data_store())

    def resolve_change_request_by_id(root, info, id):
        return change_request.ChangeRequest.get_by_primary_key_value(value=id, data_store=get_data_store())

    def resolve_system_change_request_by_id(root, info, id):
        return system_change_request.SystemChangeRequest.get_by_primary_key_value(value=id, data_store=get_data_store())

    def resolve_dedicated_team_planning_periods(root, info):
        return dedicated_team.DedicatedTeamPlanningPeriod.all(data_store=get_data_store())

    def resolve_dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
        return dedicated_team.DedicatedTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'dedicated_team_id': dedicated_team_id
        }, data_store=get_data_store())

    def resolve_project_team_planning_period_by_planning_period_id_and_project_team_id(root, info, planning_period_id, project_team_id):
        return project_team.ProjectTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'project_team_id': project_team_id
        }, data_store=get_data_store())

    def resolve_systems(root, info):
        return system.System.all(data_store=get_data_store())

    def resolve_system_planning_periods(root, info):
        return system.SystemPlanningPeriod.all(data_store=get_data_store())

    def resolve_system_planning_period_by_planning_period_id_and_system_id(root, info, planning_period_id, system_id):
        return system.SystemPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())

    def resolve_project_team_planning_period_system_by_project_team_id_planning_period_id_and_system_id(root, info, project_team_id, planning_period_id, system_id):
        return project_team.ProjectTeamPlanningPeriodSystem.get_by_multiple_fields(fields={
            'project_team_id': project_team_id,
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())

    def resolve_dedicated_team_planning_period_system_by_dedicated_team_id_planning_period_id_and_system_id(root, info, dedicated_team_id, planning_period_id, system_id):
        return dedicated_team.DedicatedTeamPlanningPeriodSystem.get_by_multiple_fields(fields={
            'dedicated_team_id': dedicated_team_id,
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())

schema = graphene.Schema(query=Query)
from django.conf import settings
import graphene
from second_eye_api.schema import change_request
from second_eye_api.schema import company
from second_eye_api.schema import dedicated_team
from second_eye_api.schema import dedicated_team_planning_period
from second_eye_api.schema import dedicated_team_quarter
from second_eye_api.schema import epic
from second_eye_api.schema import incident
from second_eye_api.schema import incident_sub_task
from second_eye_api.schema import non_project_activity
from second_eye_api.schema import person
from second_eye_api.schema import person_month
from second_eye_api.schema import person_project_team_month
from second_eye_api.schema import planning_period
from second_eye_api.schema import project_manager
from second_eye_api.schema import project_manager_month
from second_eye_api.schema import project_team
from second_eye_api.schema import project_team_planning_period
from second_eye_api.schema import project_team_quarter
from second_eye_api.schema import quarter
from second_eye_api.schema import state
from second_eye_api.schema import state_category
from second_eye_api.schema import skill
from second_eye_api.schema import system
from second_eye_api.schema import system_change_request
from second_eye_api.schema import task

def get_data_store():
    result = settings.GRAPHENE_FRAME_DATA_STORE
    return result

class Query(graphene.ObjectType):
    change_request_by_key = graphene.Field(change_request.ChangeRequest, key=graphene.String())
    def resolve_change_request_by_key(root, info, key):
        return change_request.ChangeRequest.get_by_field_value(field="key", value=key, data_store=get_data_store())

    change_requests = graphene.List(change_request.ChangeRequest)
    def resolve_change_requests(root, info):
        return change_request.ChangeRequest.all(data_store=get_data_store())

    change_requests_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter = graphene.List(
        quarter.ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter
    )
    def resolve_change_requests_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter(root, info):
        return quarter.ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter.all(data_store=get_data_store())

    companies = graphene.List(company.Company)
    def resolve_companies(root, info):
        return company.Company.all(data_store=get_data_store())

    company_by_id = graphene.Field(company.Company, id=graphene.Int())
    def resolve_company_by_id(root, info, id):
        return company.Company.get_by_primary_key_value(value=id, data_store=get_data_store())

    dedicated_team_by_id = graphene.Field(dedicated_team.DedicatedTeam, id=graphene.Int())
    def resolve_dedicated_team_by_id(root, info, id):
        return dedicated_team.DedicatedTeam.get_by_primary_key_value(value=id, data_store=get_data_store())

    dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id = graphene.Field(
        dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        dedicated_team_id=graphene.Int()
    )
    def resolve_dedicated_team_planning_period_by_planning_period_id_and_dedicated_team_id(root, info, planning_period_id, dedicated_team_id):
        return dedicated_team_planning_period.DedicatedTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'dedicated_team_id': dedicated_team_id
        }, data_store=get_data_store())

    dedicated_team_planning_period_system_by_dedicated_team_id_planning_period_id_and_system_id = graphene.Field(
        dedicated_team_planning_period.DedicatedTeamPlanningPeriodSystem,
        dedicated_team_id=graphene.Int(),
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )
    def resolve_dedicated_team_planning_period_system_by_dedicated_team_id_planning_period_id_and_system_id(root, info, dedicated_team_id, planning_period_id, system_id):
        return dedicated_team_planning_period.DedicatedTeamPlanningPeriodSystem.get_by_multiple_fields(fields={
            'dedicated_team_id': dedicated_team_id,
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())

    dedicated_team_planning_periods = graphene.List(dedicated_team_planning_period.DedicatedTeamPlanningPeriod)
    def resolve_dedicated_team_planning_periods(root, info):
        return dedicated_team_planning_period.DedicatedTeamPlanningPeriod.all(data_store=get_data_store())

    dedicated_team_quarter_by_quarter_key_and_dedicated_team_id = graphene.Field(
        dedicated_team_quarter.DedicatedTeamQuarter,
        quarter_key=graphene.String(),
        dedicated_team_id=graphene.Int()
    )
    def resolve_dedicated_team_quarter_by_quarter_key_and_dedicated_team_id(root, info, quarter_key, dedicated_team_id):
        return dedicated_team_quarter.DedicatedTeamQuarter.get_by_multiple_fields(fields={
            'quarter_key': quarter_key,
            'dedicated_team_id': dedicated_team_id
        }, data_store=get_data_store())

    dedicated_teams = graphene.List(dedicated_team.DedicatedTeam)
    def resolve_dedicated_teams(root, info):
        return dedicated_team.DedicatedTeam.all(data_store=get_data_store())

    epic_by_key = graphene.Field(epic.Epic, key=graphene.String())
    def resolve_epic_by_key(root, info, key):
        return epic.Epic.get_by_field_value(field="key", value=key, data_store=get_data_store())

    epic_system_by_epic_key_and_system_id = graphene.Field(
        epic.EpicSystem,
        epic_key=graphene.String(),
        system_id=graphene.Int()
    )
    def resolve_epic_system_by_epic_key_and_system_id(root, info, epic_key, system_id):
        return epic.EpicSystem.get_by_multiple_fields(fields={
            'epic_key': epic_key,
            'system_id': system_id
        }, data_store=get_data_store())

    epics = graphene.List(epic.Epic)
    def resolve_epics(root, info):
        return epic.Epic.all(data_store=get_data_store())

    incident_sub_task_by_key = graphene.Field(incident_sub_task.IncidentSubTask, key=graphene.String())
    def resolve_incident_sub_task_by_key(root, info, key):
        return incident_sub_task.IncidentSubTask.get_by_field_value(field="key", value=key, data_store=get_data_store())

    incident_by_key = graphene.Field(incident.Incident, key=graphene.String())
    def resolve_incident_by_key(root, info, key):
        return incident.Incident.get_by_field_value(field="key", value=key, data_store=get_data_store())

    incidents = graphene.List(incident.Incident)
    def resolve_incidents(root, info):
        return incident.Incident.all(data_store=get_data_store())

    non_project_activities = graphene.List(non_project_activity.NonProjectActivity)
    def resolve_non_project_activities(root, info):
        return non_project_activity.NonProjectActivity.all(data_store=get_data_store())

    non_project_activity_by_key = graphene.Field(non_project_activity.NonProjectActivity, key=graphene.String())
    def resolve_non_project_activity_by_key(root, info, key):
        return non_project_activity.NonProjectActivity.get_by_field_value(field="key", value=key, data_store=get_data_store())

    person_by_key = graphene.Field(person.Person, key=graphene.String())
    def resolve_person_by_key(root, info, key):
        return person.Person.get_by_field_value(field="key", value=key, data_store=get_data_store())

    person_system_change_request_time_sheets_by_date_by_person_key_and_system_change_request_key = graphene.List(
        person.PersonSystemChangeRequestTimeSheetsByDate,
        person_key=graphene.String(),
        system_change_request_key=graphene.String()
    )
    def resolve_person_system_change_request_time_sheets_by_date_by_person_key_and_system_change_request_key(root, info, person_key, system_change_request_key):
        return person.PersonSystemChangeRequestTimeSheetsByDate.filter_by_multiple_fields(fields={
            'person_key': person_key,
            'system_change_request_key': system_change_request_key,
        }, data_store=get_data_store())

    persons = graphene.List(person.Person)
    def resolve_persons(root, info):
        return person.Person.all(data_store=get_data_store())

    persons_by_project_team_id_and_month = graphene.List(
        person_project_team_month.PersonProjectTeamMonth,
        project_team_id=graphene.Int(),
        month=graphene.Date()
    )
    def resolve_persons_by_project_team_id_and_month(root, info, project_team_id, month):
        return person_project_team_month.PersonProjectTeamMonth.filter_by_multiple_fields(fields={
            'project_team_id': project_team_id,
            'month': month,
        }, data_store=get_data_store())

    person_month_by_person_key_and_month = graphene.Field(
        person_month.PersonMonthTimeSpent,
        person_key=graphene.String(),
        month=graphene.Date()
    )
    def resolve_person_month_by_person_key_and_month(root, info, person_key, month):
        return person_month.PersonMonthTimeSpent.get_by_multiple_fields(fields={
            'person_key': person_key,
            'month': month,
        }, data_store=get_data_store())

    persons_with_time_spent_for_change_requests_in_current_quarter_while_change_request_not_in_current_quarter = graphene.List(
        quarter.PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter
    )
    def resolve_persons_with_time_spent_for_change_requests_in_current_quarter_while_change_request_not_in_current_quarter(root, info):
        return quarter.PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter.all(data_store=get_data_store())

    planning_period_by_id = graphene.Field(planning_period.PlanningPeriod, id=graphene.Int())
    def resolve_planning_period_by_id(root, info, id):
        return planning_period.PlanningPeriod.get_by_primary_key_value(value=id, data_store=get_data_store())

    planning_period_person_by_planning_period_id_and_person_key = graphene.Field(
        person.PersonPlanningPeriodTimeSpent,
        planning_period_id=graphene.Int(),
        person_key=graphene.String()
    )
    def resolve_planning_period_person_by_planning_period_id_and_person_key(root, info, planning_period_id, person_key):
        return person.PersonPlanningPeriodTimeSpent.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'person_key': person_key
        }, data_store=get_data_store())

    planning_periods = graphene.List(planning_period.PlanningPeriod)
    def resolve_planning_periods(root, info):
        return planning_period.PlanningPeriod.all(data_store=get_data_store())

    project_manager_by_id = graphene.Field(project_manager.ProjectManager, id=graphene.Int())
    def resolve_project_manager_by_id(root, info, id):
        return project_manager.ProjectManager.get_by_multiple_fields(fields={
            'id': id,
        }, data_store=get_data_store())

    project_managers = graphene.List(project_manager.ProjectManager)
    def resolve_project_managers(root, info):
        return project_manager.ProjectManager.all(data_store=get_data_store())

    project_manager_months_by_project_manager_id = graphene.List(
        project_manager_month.ProjectManagerMonth,
        project_manager_id=graphene.Int()
    )
    def resolve_project_manager_months_by_project_manager_id(root, info, project_manager_id):
        return project_manager_month.ProjectManagerMonth.filter_by_multiple_fields(fields={
            'project_manager_id': project_manager_id,
        }, data_store=get_data_store())

    project_team_by_id = graphene.Field(project_team.ProjectTeam, id=graphene.Int())
    def resolve_project_team_by_id(root, info, id):
        return project_team.ProjectTeam.get_by_primary_key_value(value=id, data_store=get_data_store())

    project_team_planning_period_by_planning_period_id_and_project_team_id = graphene.Field(
        project_team_planning_period.ProjectTeamPlanningPeriod,
        planning_period_id=graphene.Int(),
        project_team_id=graphene.Int()
    )
    def resolve_project_team_planning_period_by_planning_period_id_and_project_team_id(root, info, planning_period_id, project_team_id):
        return project_team_planning_period.ProjectTeamPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'project_team_id': project_team_id
        }, data_store=get_data_store())

    project_team_planning_period_system_by_project_team_id_planning_period_id_and_system_id = graphene.Field(
        project_team_planning_period.ProjectTeamPlanningPeriodSystem,
        project_team_id=graphene.Int(),
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )
    def resolve_project_team_planning_period_system_by_project_team_id_planning_period_id_and_system_id(root, info, project_team_id, planning_period_id, system_id):
        return project_team_planning_period.ProjectTeamPlanningPeriodSystem.get_by_multiple_fields(fields={
            'project_team_id': project_team_id,
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())


    project_team_quarter_by_quarter_key_and_project_team_id = graphene.Field(
        project_team_quarter.ProjectTeamQuarter,
        quarter_key=graphene.String(),
        project_team_id=graphene.Int()
    )
    def resolve_project_team_quarter_by_quarter_key_and_project_team_id(root, info, quarter_key, project_team_id):
        return project_team_quarter.ProjectTeamQuarter.get_by_multiple_fields(fields={
            'quarter_key': quarter_key,
            'project_team_id': project_team_id
        }, data_store=get_data_store())

    project_teams = graphene.List(project_team.ProjectTeam)
    def resolve_project_teams(root, info):
        return project_team.ProjectTeam.all(data_store=get_data_store())

    quarter_by_key = graphene.Field(quarter.Quarter, key=graphene.String())
    def resolve_quarter_by_key(root, info, key):
        return quarter.Quarter.get_by_field_value(field="key", value=key, data_store=get_data_store())

    quarter_project_teams_by_quarter_key = graphene.List(
        project_team_quarter.ProjectTeamQuarter,
        quarter_key=graphene.String()
    )
    def resolve_quarter_project_teams_by_quarter_key(root, info, quarter_key):
        return project_team_quarter.ProjectTeamQuarter.filter_by_multiple_fields(fields={
            'quarter_key': quarter_key,
        }, data_store=get_data_store())

    quarters = graphene.List(quarter.Quarter)
    def resolve_quarters(root, info):
        return quarter.Quarter.all(data_store=get_data_store())

    skills = graphene.List(skill.Skill)
    def resolve_skills(root, info):
        return skill.Skill.all(data_store=get_data_store())

    state_categories = graphene.List(state_category.StateCategory)
    def resolve_state_categories(root, info):
        return state_category.StateCategory.all(data_store=get_data_store())

    state_by_id = graphene.Field(state.State, id=graphene.String())
    def resolve_state_by_id(root, info, id):
        return state.State.get_by_field_value(field="id", value=id, data_store=get_data_store())

    states = graphene.List(state.State)
    def resolve_states(root, info):
        return state.State.all(data_store=get_data_store())

    system_change_request_by_key = graphene.Field(system_change_request.SystemChangeRequest, key=graphene.String())
    def resolve_system_change_request_by_key(root, info, key):
        return system_change_request.SystemChangeRequest.get_by_field_value(field="key", value=key, data_store=get_data_store())

    system_change_requests = graphene.List(system_change_request.SystemChangeRequest)
    def resolve_system_change_requests(root, info):
        return system_change_request.SystemChangeRequest.all(data_store=get_data_store())

    system_by_id = graphene.Field(system.System, id=graphene.Int())
    def resolve_system_by_id(root, info, id):
        return system.System.get_by_primary_key_value(value=id, data_store=get_data_store())

    system_planning_period_by_planning_period_id_and_system_id = graphene.Field(
        system.SystemPlanningPeriod,
        planning_period_id=graphene.Int(),
        system_id=graphene.Int()
    )
    def resolve_system_planning_period_by_planning_period_id_and_system_id(root, info, planning_period_id, system_id):
        return system.SystemPlanningPeriod.get_by_multiple_fields(fields={
            'planning_period_id': planning_period_id,
            'system_id': system_id
        }, data_store=get_data_store())

    system_planning_periods = graphene.List(system.SystemPlanningPeriod)
    def resolve_system_planning_periods(root, info):
        return system.SystemPlanningPeriod.all(data_store=get_data_store())

    systems = graphene.List(system.System)
    def resolve_systems(root, info):
        return system.System.all(data_store=get_data_store())

    task_by_key = graphene.Field(task.Task, key=graphene.String())
    def resolve_task_by_key(root, info, key):
        return task.Task.get_by_field_value(field="key", value=key, data_store=get_data_store())

    tasks = graphene.List(task.Task)
    def resolve_tasks(root, info):
        return task.Task.all(data_store=get_data_store())

schema = graphene.Schema(query=Query)
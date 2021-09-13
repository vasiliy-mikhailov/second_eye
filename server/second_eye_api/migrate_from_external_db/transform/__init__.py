import cubista
from second_eye_api.migrate_from_external_db.transform import entities
from second_eye_api.migrate_from_external_db.output_data import OutputData
from .entities.company_transform import *
from .entities.dedicated_teams_transform import *
from .entities.project_team_transform import *
from .utils import *
from .entities.tasks_transform import *
from .entities.system_change_requests_transform import *
from .entities.change_requests_transform import *
from .entities.planning_periods_transform import *
from .entities.planning_period_time_sheets_by_date_transform import *
from .entities.planning_period_time_spent_percent_with_value_and_without_value_by_date_transform import *
from .entities.project_team_planning_periods_transform import *
from .entities.project_team_planning_period_time_sheets_by_date_transform import *
from .entities.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date_transform import *
from .entities.dedicated_team_planning_periods_transform import *
from .entities.dedicated_team_planning_period_time_sheets_by_date_transform import *
from .entities.dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date_transform import *

def calculate_time_sheets_inplace(output_data):
    output_data.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date = calculate_project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date = calculate_dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.planning_period_time_sheets_by_date = calculate_planning_period_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.planning_period_time_sheets_by_date = propagate_planning_periods_start_into_planning_period_time_sheets_by_date(
        planning_period_time_sheets_by_date=output_data.planning_period_time_sheets_by_date,
        planning_periods=output_data.planning_periods
    )

    output_data.planning_period_time_sheets_by_date = propagate_planning_periods_end_into_planning_period_time_sheets_by_date(
        planning_period_time_sheets_by_date=output_data.planning_period_time_sheets_by_date,
        planning_periods=output_data.planning_periods
    )

    output_data.planning_period_time_spent_percent_with_value_and_without_value_by_date = calculate_planning_period_time_spent_percent_with_value_and_without_value_by_date(
        task_time_sheets=output_data.task_time_sheets
    )


def calculate_companies_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.companies = calculate_companies_actual_change_request_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_actual_analysis_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_analysis_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_actual_development_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_development_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_actual_testing_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_testing_queue_length_inplace(companies=output_data.companies)

def calculate_dedicated_teams_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.dedicated_teams = calculate_dedicated_teams_actual_change_request_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_actual_analysis_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_analysis_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_actual_development_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_development_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_actual_testing_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_testing_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

def calculate_project_teams_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.project_teams = calculate_project_teams_actual_change_request_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_actual_analysis_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_analysis_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_actual_development_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_development_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_actual_testing_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_testing_queue_length_inplace(project_teams=output_data.project_teams)

def calculate_change_requests_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.change_requests = calculate_change_requests_actual_change_request_capacity_by_task_time_sheets(
        change_requests=output_data.change_requests,
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_requests = calculate_change_requests_actual_analysis_capacity_by_task_time_sheets(
        change_requests=output_data.change_requests,
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_requests = calculate_change_requests_actual_development_capacity_by_task_time_sheets(
        change_requests=output_data.change_requests,
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_requests = calculate_change_requests_actual_testing_capacity_by_task_time_sheets(
        change_requests=output_data.change_requests,
        task_time_sheets=output_data.task_time_sheets
    )

def make_planning_period_predictions(output_data):
    output_data.planning_periods = calculate_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
        planning_periods=output_data.planning_periods,
        planning_period_time_sheets_by_date=output_data.planning_period_time_sheets_by_date
    )

    calculate_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        planning_periods=output_data.planning_periods
    )

    output_data.planning_period_time_sheets_by_date = calculate_planning_period_time_spent_cumsum_prediction_by_planning_periods_m_and_b(
        planning_period_time_sheets_by_date=output_data.planning_period_time_sheets_by_date,
        planning_periods=output_data.planning_periods
    )

def make_dedicated_team_planning_period_predictions(output_data):
    output_data.dedicated_team_planning_periods = calculate_dedicated_team_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
        dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
        dedicated_team_planning_period_time_sheets_by_date=output_data.dedicated_team_planning_period_time_sheets_by_date
    )

    calculate_dedicated_team_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
    )

    output_data.dedicated_team_planning_period_time_sheets_by_date = calculate_dedicated_team_planning_period_time_spent_cumsum_prediction_by_dedicated_team_planning_periods_m_and_b(
        dedicated_team_planning_period_time_sheets_by_date=output_data.dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
    )

def make_project_team_planning_period_predictions(output_data):
    output_data.project_team_planning_periods = calculate_project_team_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
        project_team_planning_periods=output_data.project_team_planning_periods,
        project_team_planning_period_time_sheets_by_date=output_data.project_team_planning_period_time_sheets_by_date
    )

    calculate_project_team_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        project_team_planning_periods=output_data.project_team_planning_periods
    )

    output_data.project_team_planning_period_time_sheets_by_date = calculate_project_team_planning_period_time_spent_cumsum_prediction_by_project_team_planning_periods_m_and_b(
        project_team_planning_period_time_sheets_by_date=output_data.project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods=output_data.project_team_planning_periods
    )

def make_predictions(output_data):
    make_planning_period_predictions(output_data=output_data)
    make_dedicated_team_planning_period_predictions(output_data=output_data)
    make_project_team_planning_period_predictions(output_data=output_data)

class Transformer:
    def __init__(self, input_data):
        self.input_data = input_data

    def transform(self):
        input_data = self.input_data

        change_request = entities.ChangeRequest(data_frame=input_data.change_requests)
        change_request_analysis_time_sheet_by_date = entities.ChangeRequestAnalysisTimeSheetByDate()
        change_request_development_time_sheet_by_date = entities.ChangeRequestDevelopmentTimeSheetByDate()
        change_request_testing_time_sheet_by_date = entities.ChangeRequestTestingTimeSheetByDate()
        change_request_time_sheet_by_date = entities.ChangeRequestTimeSheetByDate()
        companiy = entities.Company(data_frame=input_data.companies)
        dedicated_team = entities.DedicatedTeam(data_frame=input_data.dedicated_teams)
        dedicated_team_planning_period = entities.DedicatedTeamPlanningPeriod()
        dedicated_team_planning_period_time_sheet_by_date = entities.DedicatedTeamPlanningperiodTimeSheetByDate()
        dedicated_team_position = entities.DedicatedTeamPosition(data_frame=input_data.dedicated_team_positions)
        function_component = entities.FunctionComponent(data_frame=input_data.function_components)
        function_component_kind = entities.FunctionComponentKind(data_frame=input_data.function_component_kinds)
        person = entities.Person(data_frame=input_data.persons)
        planning_period = entities.PlanningPeriod(data_frame=input_data.planning_periods)
        project_team = entities.ProjectTeam(data_frame=input_data.project_teams)
        project_team_planning_period = entities.ProjectTeamPlanningPeriod()
        project_team_planning_period_time_sheet_by_date = entities.ProjectTeamPlanningperiodTimeSheetByDate()
        project_team_position = entities.ProjectTeamPosition(data_frame=input_data.project_team_positions)
        skill = entities.Skill(data_frame=input_data.skills)
        state_category = entities.StateCategory(data_frame=input_data.state_categories)
        state = entities.State(data_frame=input_data.states)
        system = entities.System(data_frame=input_data.systems)
        system_change_request = entities.SystemChangeRequest(data_frame=input_data.system_change_requests)
        system_change_request_analysis_time_sheet_by_date = entities.SystemChangeRequestAnalysisTimeSheetByDate()
        system_change_request_development_time_sheet_by_date = entities.SystemChangeRequestDevelopmentTimeSheetByDate()
        system_change_request_testing_time_sheet_by_date = entities.SystemChangeRequestTestingTimeSheetByDate()
        system_change_request_time_sheet = entities.SystemChangeRequestTimeSheet(data_frame=input_data.system_change_request_time_sheets)
        system_change_request_time_sheet_by_date = entities.SystemChangeRequestTimeSheetByDate()
        system_planning_period = entities.SystemPlanningPeriod()
        system_planning_period_time_sheet_by_date = entities.SystemPlanningPeriodTimeSheetByDate()
        task = entities.Task(data_frame=input_data.tasks)
        task_analysis_time_sheet_by_date = entities.TaskAnalysisTimeSheetByDate()
        task_development_time_sheet_by_date = entities.TaskDevelopmentTimeSheetByDate()
        task_testing_time_sheet_by_date = entities.TaskTestingTimeSheetByDate()
        task_time_sheet = entities.TaskTimeSheet(data_frame=input_data.task_time_sheets)
        task_time_sheet_by_date = entities.TaskTimeSheetByDate()

        data_source = cubista.DataSource(tables={
            change_request,
            change_request_analysis_time_sheet_by_date,
            change_request_development_time_sheet_by_date,
            change_request_testing_time_sheet_by_date,
            change_request_time_sheet_by_date,
            companiy,
            dedicated_team,
            dedicated_team_planning_period,
            dedicated_team_planning_period_time_sheet_by_date,
            dedicated_team_position,
            function_component,
            function_component_kind,
            person,
            planning_period,
            project_team,
            project_team_planning_period,
            project_team_planning_period_time_sheet_by_date,
            project_team_position,
            skill,
            state_category,
            state,
            system,
            system_change_request,
            system_change_request_analysis_time_sheet_by_date,
            system_change_request_development_time_sheet_by_date,
            system_change_request_testing_time_sheet_by_date,
            system_change_request_time_sheet,
            system_change_request_time_sheet_by_date,
            system_planning_period,
            system_planning_period_time_sheet_by_date,
            task,
            task_analysis_time_sheet_by_date,
            task_development_time_sheet_by_date,
            task_testing_time_sheet_by_date,
            task_time_sheet,
            task_time_sheet_by_date,
        })

        print("cubista done")

        output_data = OutputData()
        output_data.change_requests = data_source.tables[entities.ChangeRequest].data_frame
        output_data.change_request_analysis_time_sheets_by_date = data_source.tables[entities.ChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.change_request_development_time_sheets_by_date = data_source.tables[entities.ChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.change_request_testing_time_sheets_by_date = data_source.tables[entities.ChangeRequestTestingTimeSheetByDate].data_frame
        output_data.change_request_time_sheets_by_date = data_source.tables[entities.ChangeRequestTimeSheetByDate].data_frame
        output_data.companies = data_source.tables[entities.Company].data_frame
        output_data.dedicated_team_planning_periods = data_source.tables[entities.DedicatedTeamPlanningPeriod].data_frame
        output_data.dedicated_team_planning_period_time_sheets_by_date = data_source.tables[entities.DedicatedTeamPlanningperiodTimeSheetByDate].data_frame
        output_data.dedicated_team_positions = data_source.tables[entities.DedicatedTeamPosition].data_frame
        output_data.dedicated_teams = data_source.tables[entities.DedicatedTeam].data_frame
        output_data.function_components = data_source.tables[entities.FunctionComponent].data_frame
        output_data.function_component_kinds = data_source.tables[entities.FunctionComponentKind].data_frame
        output_data.persons = data_source.tables[entities.Person].data_frame
        output_data.planning_periods = data_source.tables[entities.PlanningPeriod].data_frame
        output_data.project_team_planning_period_time_sheets_by_date = data_source.tables[entities.ProjectTeamPlanningperiodTimeSheetByDate].data_frame
        output_data.project_team_planning_periods = data_source.tables[entities.ProjectTeamPlanningPeriod].data_frame
        output_data.project_team_positions = data_source.tables[entities.ProjectTeamPosition].data_frame
        output_data.project_teams = data_source.tables[entities.ProjectTeam].data_frame
        output_data.skills = data_source.tables[entities.Skill].data_frame
        output_data.states = data_source.tables[entities.State].data_frame
        output_data.state_categories = data_source.tables[entities.StateCategory].data_frame
        output_data.systems = data_source.tables[entities.System].data_frame
        output_data.system_change_requests = data_source.tables[entities.SystemChangeRequest].data_frame
        output_data.system_change_request_analysis_time_sheets_by_date = data_source.tables[entities.SystemChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.system_change_request_development_time_sheets_by_date = data_source.tables[entities.SystemChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.system_change_request_testing_time_sheets_by_date = data_source.tables[entities.SystemChangeRequestTestingTimeSheetByDate].data_frame
        output_data.system_change_request_time_sheets = data_source.tables[entities.SystemChangeRequestTimeSheet].data_frame
        output_data.system_change_request_time_sheets_by_date = data_source.tables[entities.SystemChangeRequestTimeSheetByDate].data_frame
        output_data.system_planning_periods = data_source.tables[entities.SystemPlanningPeriod].data_frame
        output_data.system_planning_period_time_sheets_by_date = data_source.tables[entities.SystemPlanningPeriodTimeSheetByDate].data_frame
        output_data.task_analysis_time_sheets_by_date = data_source.tables[entities.TaskAnalysisTimeSheetByDate].data_frame
        output_data.task_development_time_sheets_by_date = data_source.tables[entities.TaskDevelopmentTimeSheetByDate].data_frame
        output_data.task_testing_time_sheets_by_date = data_source.tables[entities.TaskTestingTimeSheetByDate].data_frame
        output_data.task_time_sheets = data_source.tables[entities.TaskTimeSheet].data_frame
        output_data.task_time_sheets_by_date = data_source.tables[entities.TaskTimeSheetByDate].data_frame
        output_data.tasks = data_source.tables[entities.Task].data_frame

        output_data.dedicated_team_position_abilities = input_data.dedicated_team_position_abilities
        output_data.project_team_position_abilities = input_data.project_team_position_abilities

        output_data.system_change_requests = make_filler_system_change_requests_summing_up_to_change_request_estimate(
            system_change_requests=output_data.system_change_requests,
            change_requests=output_data.change_requests
        )

        output_data.tasks = make_filler_tasks_summing_up_to_system_change_request_estimate(
            tasks=output_data.tasks,
            system_change_requests=output_data.system_change_requests
        )

        calculate_time_sheets_inplace(output_data=output_data)

        make_predictions(output_data=output_data)

        calculate_companies_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_dedicated_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_project_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_change_requests_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        return output_data
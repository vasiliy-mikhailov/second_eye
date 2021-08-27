from second_eye_api.migrate_from_external_db.output_data import OutputData

from .entities.company_transform import *
from .entities.dedicated_teams_transform import *
from .entities.project_team_transform import *
from .utils import *
from .entities.states_transform import *
from .entities.function_components_transform import *
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
from .entities.dedicated_team_positions_transform import *
from .entities.project_team_positions_transform import *
from .entities.task_time_sheets_transform import *
from .entities.change_request_time_sheets_by_date_transform import *
from .entities.system_change_request_time_sheets_by_date_transform import *
from .entities.task_time_sheets_by_date_transform import *


def fix_broken_links(output_data):
    output_data.task_time_sheets = remove_task_time_sheets_not_referencing_any_task_by_id(
        tasks_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    replace_broken_system_change_request_system_id_to_system_id_with_minus_one(
        system_change_requests=output_data.system_change_requests,
        systems=output_data.systems
    )

    replace_broken_system_change_request_change_request_id_to_change_request_id_with_minus_one(
        system_change_requests=output_data.system_change_requests,
        change_requests=output_data.change_requests
    )

    replace_broken_task_system_change_request_id_to_system_change_request_id_with_minus_one(
        tasks=output_data.tasks,
        system_change_requests=output_data.system_change_requests
    )

    replace_broken_dedicated_team_positions_person_id_to_persons_id_with_minus_one(
        dedicated_team_positions=output_data.dedicated_team_positions,
        persons=output_data.persons
    )

    replace_broken_project_team_positions_person_id_to_persons_id_with_minus_one(
        project_team_positions=output_data.project_team_positions,
        persons=output_data.persons
    )

    replace_broken_function_component_task_id_to_task_id_with_minus_one(
        function_components=output_data.function_components,
        tasks=output_data.tasks
    )

    replace_broken_task_time_sheet_task_id_to_task_id_with_minus_one(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    replace_broken_task_time_sheet_person_id_to_person_id_with_minus_one(
        task_time_sheets=output_data.task_time_sheets,
        persons=output_data.persons
    )

def propagate_state_category_into_change_requests_system_change_requests_tasks_and_function_components(output_data):
    output_data.change_requests = propagate_state_category_id_into_change_requests(
        change_requests=output_data.change_requests,
        states=output_data.states
    )

    output_data.system_change_requests = propagate_state_category_id_into_system_change_requests(
        system_change_requests=output_data.system_change_requests,
        states=output_data.states
    )

    output_data.tasks = propagate_state_category_id_into_tasks(
        tasks=output_data.tasks,
        states=output_data.states
    )

    output_data.function_components = propagate_state_category_id_into_function_components(
        function_components=output_data.function_components,
        states=output_data.states
    )

def propagate_dedicated_team_company_id_to_project_teams_change_requests_system_change_requests_and_tasks(output_data):
    output_data.project_teams = propagate_dedicated_teams_company_id_into_project_teams(
        project_teams=output_data.project_teams, dedicated_teams=output_data.dedicated_teams
    )

    output_data.change_requests = propagate_project_teams_company_id_into_change_requests(
        change_requests=output_data.change_requests, project_teams=output_data.project_teams
    )

    output_data.system_change_requests = propagate_change_requests_company_id_into_system_change_requests(
        system_change_requests=output_data.system_change_requests, change_requests=output_data.change_requests
    )

    output_data.tasks = propagate_system_change_requests_company_id_into_tasks(
        tasks=output_data.tasks, system_change_requests=output_data.system_change_requests
    )


def propagate_project_team_dedicated_team_id_to_change_requests_system_change_requests_and_tasks(output_data):
    output_data.change_requests = propagate_project_teams_dedicated_team_id_into_change_requests(
        change_requests=output_data.change_requests, project_teams=output_data.project_teams
    )

    output_data.system_change_requests = propagate_change_requests_dedicated_team_id_into_system_change_requests(
        system_change_requests=output_data.system_change_requests, change_requests=output_data.change_requests
    )

    output_data.tasks = propagate_system_change_requests_dedicated_team_id_into_tasks(
        tasks=output_data.tasks, system_change_requests=output_data.system_change_requests
    )

def propagate_change_request_project_team_to_system_change_requests_and_tasks(output_data):
    output_data.system_change_requests = propagate_change_requests_project_team_id_into_system_change_requests(
        system_change_requests=output_data.system_change_requests, change_requests=output_data.change_requests
    )

    output_data.tasks = propagate_system_change_requests_project_team_id_into_tasks(
        tasks=output_data.tasks, system_change_requests=output_data.system_change_requests
    )

def propagate_change_request_planning_period_id_to_system_change_requests_and_tasks(output_data):
    output_data.system_change_requests = propagate_change_requests_planning_period_id_into_system_change_requests(
        system_change_requests=output_data.system_change_requests,
        change_requests=output_data.change_requests
    )

    output_data.tasks = propagate_system_change_requests_planning_period_id_into_tasks(
        tasks=output_data.tasks,
        system_change_requests=output_data.system_change_requests
    )

def propagate_change_request_has_value_to_system_change_requests_and_tasks(output_data):
    output_data.system_change_requests = propagate_change_requests_has_value_into_system_change_requests(
        system_change_requests=output_data.system_change_requests,
        change_requests=output_data.change_requests
    )

    output_data.tasks = propagate_system_change_requests_has_value_into_tasks(
        tasks=output_data.tasks,
        system_change_requests=output_data.system_change_requests
    )

def calculate_time_sheets_inplace(output_data):
    output_data.task_time_sheets = propagate_task_company_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )


    output_data.task_time_sheets = propagate_task_skill_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    output_data.task_time_sheets = propagate_task_planning_period_id_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    output_data.task_time_sheets = propagate_task_system_change_request_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    output_data.task_time_sheets = propagate_system_change_request_change_request_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        system_change_requests=output_data.system_change_requests
    )

    output_data.task_time_sheets = propagate_change_request_project_team_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        change_requests=output_data.change_requests
    )

    output_data.task_time_sheets = propagate_project_team_dedicated_team_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        project_teams=output_data.project_teams
    )

    output_data.task_time_sheets = propagate_project_team_planning_period_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    output_data.task_time_sheets = propagate_dedicated_team_planning_period_id_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        tasks=output_data.tasks
    )

    output_data.task_time_sheets = propagate_change_request_has_value_into_task_time_sheets(
        task_time_sheets=output_data.task_time_sheets,
        change_requests=output_data.change_requests
    )

    output_data.task_time_sheets_by_date = calculate_task_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.system_change_request_analysis_time_sheets_by_date = calculate_system_change_request_analysis_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.system_change_request_development_time_sheets_by_date = calculate_system_change_request_development_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.system_change_request_testing_time_sheets_by_date = calculate_system_change_request_testing_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.system_change_request_time_sheets_by_date = calculate_system_change_request_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_request_analysis_time_sheets_by_date = calculate_change_request_analysis_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_request_development_time_sheets_by_date = calculate_change_request_development_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_request_testing_time_sheets_by_date = calculate_change_request_testing_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.change_request_time_sheets_by_date = calculate_change_request_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.project_team_planning_period_time_sheets_by_date = calculate_project_team_planning_period_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.project_team_planning_period_time_sheets_by_date = propagate_project_team_planning_period_planning_period_start_into_project_team_planning_period_time_sheets_by_date(
        project_team_planning_period_time_sheets_by_date=output_data.project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods=output_data.project_team_planning_periods
    )

    output_data.project_team_planning_period_time_sheets_by_date = propagate_project_team_planning_period_planning_period_end_into_project_team_planning_period_time_sheets_by_date(
        project_team_planning_period_time_sheets_by_date=output_data.project_team_planning_period_time_sheets_by_date,
        project_team_planning_periods=output_data.project_team_planning_periods
    )


    output_data.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date = calculate_project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.dedicated_team_planning_period_time_sheets_by_date = calculate_dedicated_team_planning_period_time_sheets_by_date(
        task_time_sheets=output_data.task_time_sheets
    )

    output_data.dedicated_team_planning_period_time_sheets_by_date = propagate_dedicated_team_planning_period_planning_period_start_into_dedicated_team_planning_period_time_sheets_by_date(
        dedicated_team_planning_period_time_sheets_by_date=output_data.dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
    )

    output_data.dedicated_team_planning_period_time_sheets_by_date = propagate_dedicated_team_planning_period_planning_period_end_into_dedicated_team_planning_period_time_sheets_by_date(
        dedicated_team_planning_period_time_sheets_by_date=output_data.dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
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
    output_data.companies = calculate_companies_time_left_by_tasks_time_left(
        companies=output_data.companies,
        tasks=output_data.tasks
    )

    output_data.companies = calculate_companies_actual_change_request_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_analysis_time_left_by_tasks_time_left(
        companies=output_data.companies,
        tasks=output_data.tasks
    )

    output_data.companies = calculate_companies_actual_analysis_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_analysis_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_development_time_left_by_tasks_time_left(
        companies=output_data.companies,
        tasks=output_data.tasks
    )

    output_data.companies = calculate_companies_actual_development_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_development_queue_length_inplace(companies=output_data.companies)

    output_data.companies = calculate_companies_testing_time_left_by_tasks_time_left(
        companies=output_data.companies,
        tasks=output_data.tasks
    )

    output_data.companies = calculate_companies_actual_testing_capacity_by_task_time_sheets(
        companies=output_data.companies,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_companies_testing_queue_length_inplace(companies=output_data.companies)

def calculate_dedicated_teams_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.dedicated_teams = calculate_dedicated_teams_time_left_by_tasks_time_left(
        dedicated_teams=output_data.dedicated_teams,
        tasks=output_data.tasks
    )

    output_data.dedicated_teams = calculate_dedicated_teams_actual_change_request_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_analysis_time_left_by_tasks_time_left(
        dedicated_teams=output_data.dedicated_teams,
        tasks=output_data.tasks
    )

    output_data.dedicated_teams = calculate_dedicated_teams_actual_analysis_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_analysis_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_development_time_left_by_tasks_time_left(
        dedicated_teams=output_data.dedicated_teams,
        tasks=output_data.tasks
    )

    output_data.dedicated_teams = calculate_dedicated_teams_actual_development_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_development_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

    output_data.dedicated_teams = calculate_dedicated_teams_testing_time_left_by_tasks_time_left(
        dedicated_teams=output_data.dedicated_teams,
        tasks=output_data.tasks
    )

    output_data.dedicated_teams = calculate_dedicated_teams_actual_testing_capacity_by_task_time_sheets(
        dedicated_teams=output_data.dedicated_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_dedicated_teams_testing_queue_length_inplace(dedicated_teams=output_data.dedicated_teams)

def calculate_project_teams_actual_change_request_capacity_effort_and_queue_length(output_data):
    output_data.project_teams = calculate_project_teams_time_left_by_tasks_time_left(
        project_teams=output_data.project_teams,
        tasks=output_data.tasks
    )

    output_data.project_teams = calculate_project_teams_actual_change_request_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_analysis_time_left_by_tasks_time_left(
        project_teams=output_data.project_teams,
        tasks=output_data.tasks
    )

    output_data.project_teams = calculate_project_teams_actual_analysis_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_analysis_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_development_time_left_by_tasks_time_left(
        project_teams=output_data.project_teams,
        tasks=output_data.tasks
    )

    output_data.project_teams = calculate_project_teams_actual_development_capacity_by_task_time_sheets(
        project_teams=output_data.project_teams,
        task_time_sheets=output_data.task_time_sheets
    )

    calculate_project_teams_development_queue_length_inplace(project_teams=output_data.project_teams)

    output_data.project_teams = calculate_project_teams_testing_time_left_by_tasks_time_left(
        project_teams=output_data.project_teams,
        tasks=output_data.tasks
    )

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

        output_data = OutputData()
        output_data.skills = input_data.skills
        output_data.systems = input_data.systems
        output_data.companies = input_data.companies
        output_data.dedicated_teams = input_data.dedicated_teams
        output_data.project_teams = input_data.project_teams
        output_data.state_categories = input_data.state_categories
        output_data.states = input_data.states
        output_data.change_requests = input_data.change_requests
        output_data.system_change_requests = input_data.system_change_requests
        output_data.function_component_kinds = input_data.function_component_kinds
        output_data.tasks = input_data.tasks
        output_data.function_components = input_data.function_components
        output_data.persons = input_data.persons
        output_data.dedicated_team_positions = input_data.dedicated_team_positions
        output_data.project_team_positions = input_data.project_team_positions
        output_data.dedicated_team_position_abilities = input_data.dedicated_team_position_abilities
        output_data.project_team_position_abilities = input_data.project_team_position_abilities
        output_data.task_time_sheets = input_data.task_time_sheets
        output_data.planning_periods = input_data.planning_periods

        fix_broken_links(output_data=output_data)

        calculate_state_category_for_states_inplace(
            states=output_data.states
        )

        propagate_state_category_into_change_requests_system_change_requests_tasks_and_function_components(
            output_data=output_data
        )

        output_data.function_components = propagate_function_component_kind_function_points_into_function_component(
            function_components=output_data.function_components,
            function_component_kinds=output_data.function_component_kinds
        )

        calculate_function_components_function_points_using_count_and_kind_function_points_inplace(function_components=output_data.function_components)

        output_data.tasks = calculate_tasks_time_spent_by_task_time_sheets(
            tasks=output_data.tasks,
            task_time_sheets=output_data.task_time_sheets
        )

        calculate_tasks_estimate_using_time_spent_state_category_id_planned_estimate_and_preliminary_estimate_inplace(tasks=output_data.tasks)

        calculate_tasks_time_left_using_estimate_and_time_spent_inplace(tasks=output_data.tasks)

        output_data.tasks = propagate_system_change_requests_system_id_into_tasks(
            tasks=output_data.tasks,
            system_change_requests=output_data.system_change_requests
        )

        output_data.system_change_requests = calculate_system_change_requests_analysis_tasks_estimate_sum(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        output_data.system_change_requests = calculate_system_change_requests_development_tasks_estimate_sum(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        output_data.system_change_requests = calculate_system_change_requests_testing_tasks_estimate_sum(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        calculate_system_change_requests_tasks_estimate_sum_using_analysis_tasks_estimate_sum_development_tasks_estimate_sum_and_testing_tasks_estimate_sum_inplace(
            system_change_requests=output_data.system_change_requests
        )

        output_data.system_change_requests = calculate_system_change_requests_analysis_time_spent(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        output_data.system_change_requests = calculate_system_change_requests_development_time_spent(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        output_data.system_change_requests = calculate_system_change_requests_testing_time_spent(
            system_change_requests=output_data.system_change_requests,
            tasks=output_data.tasks
        )

        calculate_system_change_requests_time_spent_using_analysis_time_spent_development_time_spent_and_testing_time_spent_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_analysis_estimate_using_analysis_time_spent_state_category_id_analysis_planned_estimate_analysis_preliminary_estimate_and_analysis_tasks_estimate_sum_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_development_estimate_using_development_time_spent_state_category_id_development_planned_estimate_development_preliminary_estimate_and_development_tasks_estimate_sum_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_testing_estimate_using_testing_time_spent_state_category_id_testing_planned_estimate_testing_preliminary_estimate_and_testing_tasks_estimate_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_estimate_using_analysis_estimate_development_estimate_and_testing_estimate_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_analysis_time_left_using_analysis_estimate_and_analysis_time_spent_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_development_time_left_using_development_estimate_and_development_time_spent_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_testing_time_left_using_testing_estimate_and_testing_time_spent_inplace(
            system_change_requests=output_data.system_change_requests
        )

        calculate_system_change_requests_time_left_using_estimate_and_time_left_inplace(
            system_change_requests=output_data.system_change_requests
        )

        output_data.change_requests = calculate_change_requests_system_change_requests_analysis_estimate_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        output_data.change_requests = calculate_change_requests_system_change_requests_development_estimate_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        output_data.change_requests = calculate_change_requests_system_change_requests_testing_estimate_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        calculate_change_requests_system_change_requests_estimate_sum_using_system_change_requests_analysis_development_and_testing_estimate_sum(
            change_requests=output_data.change_requests
        )

        output_data.change_requests = calculate_change_requests_analysis_time_spent_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        output_data.change_requests = calculate_change_requests_development_time_spent_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        output_data.change_requests = calculate_change_requests_testing_time_spent_sum(
            change_requests=output_data.change_requests,
            system_change_requests=output_data.system_change_requests
        )

        calculate_change_requests_time_spent_using_analysis_development_and_testing_time_spent_inplace(
            change_requests=output_data.change_requests
        )

        calculate_change_requests_analysis_estimate_using_analysis_time_spent_state_category_id_analysis_express_estimate_and_system_change_requests_analysis_estimate_sum_inplace(
            change_requests=output_data.change_requests
        )

        calculate_change_requests_development_estimate_using_development_time_spent_state_category_id_development_express_estimate_and_system_change_requests_development_estimate_sum_inplace(
            change_requests=output_data.change_requests
        )

        calculate_change_requests_testing_estimate_using_testing_time_spent_state_category_id_testing_express_estimate_and_system_change_requests_testing_estimate_sum_inplace(
            change_requests=output_data.change_requests
        )

        calculate_change_requests_estimate_using_analysis_development_and_testing_estimate_inplace(
            change_requests=output_data.change_requests
        )

        calculate_change_requests_analyis_time_left_using_analysis_estimate_and_analysis_time_spent_inplace(change_requests=output_data.change_requests)
        calculate_change_requests_development_time_left_using_development_estimate_and_development_time_spent_inplace(change_requests=output_data.change_requests)
        calculate_change_requests_testing_time_left_using_testing_estimate_and_testing_time_spent_inplace(change_requests=output_data.change_requests)
        calculate_change_requests_time_left_using_analysis_development_and_testing_time_left(change_requests=output_data.change_requests)

        output_data.system_change_requests = make_filler_system_change_requests_summing_up_to_change_request_estimate(
            system_change_requests=output_data.system_change_requests,
            change_requests=output_data.change_requests
        )

        output_data.tasks = make_filler_tasks_summing_up_to_system_change_request_estimate(
            tasks=output_data.tasks,
            system_change_requests=output_data.system_change_requests
        )

        calculate_change_requests_planning_period_using_planning_period_id_planned_install_date_and_year_label_max_inplace(change_requests=output_data.change_requests)

        calculate_planning_periods_name_using_id_inplace(planning_periods=output_data.planning_periods)
        calculate_planning_periods_start_using_id_inplace(planning_periods=output_data.planning_periods)
        calculate_planning_periods_end_using_id_inplace(planning_periods=output_data.planning_periods)

        propagate_dedicated_team_company_id_to_project_teams_change_requests_system_change_requests_and_tasks(output_data=output_data)

        propagate_project_team_dedicated_team_id_to_change_requests_system_change_requests_and_tasks(output_data=output_data)

        propagate_change_request_project_team_to_system_change_requests_and_tasks(output_data=output_data)

        propagate_change_request_planning_period_id_to_system_change_requests_and_tasks(output_data=output_data)

        propagate_change_request_has_value_to_system_change_requests_and_tasks(output_data=output_data)

        output_data.tasks = propagate_system_change_requests_change_request_id_into_tasks(
            tasks=output_data.tasks,
            system_change_requests=output_data.system_change_requests
        )

        output_data.project_team_planning_periods = calculate_project_team_planning_periods_from_change_requests_planning_period_id_and_project_team_id(
            change_requests=output_data.change_requests
        )

        output_data.project_team_planning_periods = calculate_project_team_planning_periods_estimate_by_tasks_estimate(
            project_team_planning_periods=output_data.project_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.project_team_planning_periods = calculate_project_team_planning_periods_time_spent_by_tasks_time_spent(
            project_team_planning_periods=output_data.project_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.project_team_planning_periods = calculate_project_team_planning_periods_time_left_by_tasks_time_left(
            project_team_planning_periods=output_data.project_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.dedicated_team_planning_periods = calculate_dedicated_team_planning_periods_from_change_requests_planning_period_id_and_dedicated_team(
            change_requests=output_data.change_requests
        )

        output_data.dedicated_team_planning_periods = calculate_dedicated_team_planning_periods_estimate_by_tasks_estimate(
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.dedicated_team_planning_periods = calculate_dedicated_team_planning_periods_time_spent_by_tasks_time_spent(
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.dedicated_team_planning_periods = calculate_dedicated_team_planning_periods_time_left_by_tasks_time_left(
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
            tasks=output_data.tasks
        )

        output_data.dedicated_team_planning_periods = propagate_planning_periods_start_into_dedicated_team_planning_periods(
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
            planning_periods=output_data.planning_periods
        )

        output_data.dedicated_team_planning_periods = propagate_planning_periods_end_into_dedicated_team_planning_periods(
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods,
            planning_periods=output_data.planning_periods
        )

        output_data.project_team_planning_periods = propagate_dedicated_team_planning_period_id_by_dedicated_team_id_and_planning_period_id_into_project_team_planning_periods(
            project_team_planning_periods=output_data.project_team_planning_periods,
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
        )

        output_data.project_team_planning_periods = propagate_planning_periods_start_into_project_team_planning_periods(
            project_team_planning_periods=output_data.project_team_planning_periods,
            planning_periods=output_data.planning_periods
        )

        output_data.project_team_planning_periods = propagate_planning_periods_end_into_project_team_planning_periods(
            project_team_planning_periods=output_data.project_team_planning_periods,
            planning_periods=output_data.planning_periods
        )

        output_data.tasks = propagate_project_team_planning_period_id_by_project_team_id_and_planning_period_id_into_tasks(
            tasks=output_data.tasks,
            project_team_planning_periods=output_data.project_team_planning_periods
        )

        output_data.tasks = propagate_dedicated_team_planning_period_id_by_dedicated_team_id_and_planning_period_id_into_tasks(
            tasks=output_data.tasks,
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
        )

        output_data.change_requests = propagate_project_team_planning_period_id_into_change_requests(
            change_requests=output_data.change_requests,
            project_team_planning_periods=output_data.project_team_planning_periods
        )

        output_data.change_requests = propagate_dedicated_team_planning_period_id_into_change_requests(
            change_requests=output_data.change_requests,
            dedicated_team_planning_periods=output_data.dedicated_team_planning_periods
        )

        output_data.planning_periods = calculate_planning_periods_estimate_using_tasks_estimate(
            planning_periods=output_data.planning_periods,
            tasks=output_data.tasks
        )

        output_data.planning_periods = calculate_planning_periods_time_spent_using_tasks_time_spent(
            planning_periods=output_data.planning_periods,
            tasks=output_data.tasks
        )

        output_data.planning_periods = calculate_planning_periods_time_left_using_tasks_time_left(
            planning_periods=output_data.planning_periods,
            tasks=output_data.tasks
        )

        calculate_time_sheets_inplace(output_data=output_data)

        make_predictions(output_data=output_data)

        calculate_companies_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_dedicated_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_project_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_change_requests_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        return output_data
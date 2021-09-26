import cubista
from .change_request import *
from .change_requests_transform import *
from .company import *
from .company_transform import *
from .dedicated_team import *
from .dedicated_teams_transform import *
from .function_component import *
from .person import *
from .planning_period import *
from .planning_period_time_sheet_by_date_model import *
from .project_team import *
from .project_team_transform import *
from .skill import *
from .state import *
from .system import *
from .system_change_request import *
from .system_change_requests_transform import *
from .task import *
from .tasks_transform import *
from .utils import *
from ..output_data import OutputData

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

class Transformer:
    def __init__(self, input_data):
        self.input_data = input_data

    def transform(self):
        input_data = self.input_data

        change_request = ChangeRequest(data_frame=input_data.change_requests)
        change_request_analysis_time_sheet_by_date = ChangeRequestAnalysisTimeSheetByDate()
        change_request_development_time_sheet_by_date = ChangeRequestDevelopmentTimeSheetByDate()
        change_request_testing_time_sheet_by_date = ChangeRequestTestingTimeSheetByDate()
        change_request_time_sheet_by_date = ChangeRequestTimeSheetByDate()
        companiy = Company(data_frame=input_data.companies)
        dedicated_team = DedicatedTeam(data_frame=input_data.dedicated_teams)
        dedicated_team_planning_period = DedicatedTeamPlanningPeriod()
        dedicated_team_planning_period_system = DedicatedTeamPlanningPeriodSystem()
        dedicated_team_planning_period_system_time_sheet_by_date = DedicatedTeamPlanningPeriodSystemTimeSheetByDate()
        dedicated_team_planning_period_system_time_sheet_by_date_model = DedicatedTeamPlanningPeriodSystemTimeSheetByDateModel()
        dedicated_team_planning_period_time_sheet_by_date = DedicatedTeamPlanningPeriodTimeSheetByDate()
        dedicated_team_planning_period_time_sheet_by_date_model = DedicatedTeamPlanningPeriodTimeSheetByDateModel()
        dedicated_team_position = DedicatedTeamPosition(data_frame=input_data.dedicated_team_positions)
        function_component = FunctionComponent(data_frame=input_data.function_components)
        function_component_kind = FunctionComponentKind(data_frame=input_data.function_component_kinds)
        person = Person(data_frame=input_data.persons)
        planning_period = PlanningPeriod(data_frame=input_data.planning_periods)
        planning_period_time_sheet_by_date = PlanningPeriodTimeSheetByDate()
        planning_period_time_sheet_by_date_model = PlanningPeriodTimeSheetByDateModel()
        project_team = ProjectTeam(data_frame=input_data.project_teams)
        project_team_planning_period = ProjectTeamPlanningPeriod()
        project_team_planning_period_system = ProjectTeamPlanningPeriodSystem()
        project_team_planning_period_system_time_sheet_by_date = ProjectTeamPlanningPeriodSystemTimeSheetByDate()
        project_team_planning_period_system_time_sheet_by_date_model = ProjectTeamPlanningPeriodSystemTimeSheetByDateModel()
        project_team_planning_period_time_sheet_by_date = ProjectTeamPlanningPeriodTimeSheetByDate()
        project_team_planning_period_time_sheet_by_date_model = ProjectTeamPlanningPeriodTimeSheetByDateModel()
        project_team_position = ProjectTeamPosition(data_frame=input_data.project_team_positions)
        skill = Skill(data_frame=input_data.skills)
        state_category = StateCategory(data_frame=input_data.state_categories)
        state = State(data_frame=input_data.states)
        system = System(data_frame=input_data.systems)
        system_change_request = SystemChangeRequest(data_frame=input_data.system_change_requests)
        system_change_request_analysis_time_sheet_by_date = SystemChangeRequestAnalysisTimeSheetByDate()
        system_change_request_development_time_sheet_by_date = SystemChangeRequestDevelopmentTimeSheetByDate()
        system_change_request_testing_time_sheet_by_date = SystemChangeRequestTestingTimeSheetByDate()
        system_change_request_time_sheet = SystemChangeRequestTimeSheet(data_frame=input_data.system_change_request_time_sheets)
        system_change_request_time_sheet_by_date = SystemChangeRequestTimeSheetByDate()
        system_planning_period = SystemPlanningPeriod()
        system_planning_period_time_sheet_by_date = SystemPlanningPeriodTimeSheetByDate()
        system_planning_period_time_sheet_by_date_model = SystemPlanningPeriodTimeSheetByDateModel()
        system_planning_period_analysis_time_sheet_by_date = SystemPlanningPeriodAnalysisTimeSheetByDate()
        system_planning_period_analysis_time_sheet_by_date_model = SystemPlanningPeriodAnalysisTimeSheetByDateModel()
        system_planning_period_development_time_sheet_by_date = SystemPlanningPeriodDevelopmentTimeSheetByDate()
        system_planning_period_development_time_sheet_by_date_model = SystemPlanningPeriodDevelopmentTimeSheetByDateModel()
        system_planning_period_testing_time_sheet_by_date = SystemPlanningPeriodTestingTimeSheetByDate()
        system_planning_period_testing_time_sheet_by_date_model = SystemPlanningPeriodTestingTimeSheetByDateModel()
        task = Task(data_frame=input_data.tasks)
        task_analysis_time_sheet_by_date = TaskAnalysisTimeSheetByDate()
        task_development_time_sheet_by_date = TaskDevelopmentTimeSheetByDate()
        task_testing_time_sheet_by_date = TaskTestingTimeSheetByDate()
        task_time_sheet = TaskTimeSheet(data_frame=input_data.task_time_sheets)
        task_time_sheet_by_date = TaskTimeSheetByDate()

        data_source = cubista.DataSource(tables={
            change_request,
            change_request_analysis_time_sheet_by_date,
            change_request_development_time_sheet_by_date,
            change_request_testing_time_sheet_by_date,
            change_request_time_sheet_by_date,
            companiy,
            dedicated_team,
            dedicated_team_planning_period,
            dedicated_team_planning_period_system,
            dedicated_team_planning_period_system_time_sheet_by_date,
            dedicated_team_planning_period_system_time_sheet_by_date_model,
            dedicated_team_planning_period_time_sheet_by_date,
            dedicated_team_planning_period_time_sheet_by_date_model,
            dedicated_team_position,
            function_component,
            function_component_kind,
            person,
            planning_period,
            planning_period_time_sheet_by_date,
            planning_period_time_sheet_by_date_model,
            project_team,
            project_team_planning_period,
            project_team_planning_period_system,
            project_team_planning_period_system_time_sheet_by_date,
            project_team_planning_period_system_time_sheet_by_date_model,
            project_team_planning_period_time_sheet_by_date,
            project_team_planning_period_time_sheet_by_date_model,
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
            system_planning_period_time_sheet_by_date_model,
            system_planning_period_analysis_time_sheet_by_date,
            system_planning_period_analysis_time_sheet_by_date_model,
            system_planning_period_development_time_sheet_by_date,
            system_planning_period_development_time_sheet_by_date_model,
            system_planning_period_testing_time_sheet_by_date,
            system_planning_period_testing_time_sheet_by_date_model,
            task,
            task_analysis_time_sheet_by_date,
            task_development_time_sheet_by_date,
            task_testing_time_sheet_by_date,
            task_time_sheet,
            task_time_sheet_by_date,
        })

        print("cubista done")

        output_data = OutputData()
        output_data.change_requests = data_source.tables[ChangeRequest].data_frame
        output_data.change_request_analysis_time_sheets_by_date = data_source.tables[ChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.change_request_development_time_sheets_by_date = data_source.tables[ChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.change_request_testing_time_sheets_by_date = data_source.tables[ChangeRequestTestingTimeSheetByDate].data_frame
        output_data.change_request_time_sheets_by_date = data_source.tables[ChangeRequestTimeSheetByDate].data_frame
        output_data.companies = data_source.tables[Company].data_frame
        output_data.dedicated_team_planning_periods = data_source.tables[DedicatedTeamPlanningPeriod].data_frame
        output_data.dedicated_team_planning_period_systems = data_source.tables[DedicatedTeamPlanningPeriodSystem].data_frame
        output_data.dedicated_team_planning_period_system_time_sheets_by_date = data_source.tables[DedicatedTeamPlanningPeriodSystemTimeSheetByDate].data_frame
        output_data.dedicated_team_planning_period_system_time_sheet_by_date_model = data_source.tables[DedicatedTeamPlanningPeriodSystemTimeSheetByDateModel].data_frame
        output_data.dedicated_team_planning_period_time_sheets_by_date = data_source.tables[DedicatedTeamPlanningPeriodTimeSheetByDate].data_frame
        output_data.dedicated_team_planning_period_time_sheets_by_date_model = data_source.tables[DedicatedTeamPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.dedicated_team_positions = data_source.tables[DedicatedTeamPosition].data_frame
        output_data.dedicated_teams = data_source.tables[DedicatedTeam].data_frame
        output_data.function_components = data_source.tables[FunctionComponent].data_frame
        output_data.function_component_kinds = data_source.tables[FunctionComponentKind].data_frame
        output_data.persons = data_source.tables[Person].data_frame
        output_data.planning_period_time_sheets_by_date = data_source.tables[PlanningPeriodTimeSheetByDate].data_frame
        output_data.planning_period_time_sheets_by_date_model = data_source.tables[PlanningPeriodTimeSheetByDateModel].data_frame
        output_data.planning_periods = data_source.tables[PlanningPeriod].data_frame
        output_data.project_team_planning_period_time_sheets_by_date = data_source.tables[ProjectTeamPlanningPeriodTimeSheetByDate].data_frame
        output_data.project_team_planning_period_time_sheet_by_date_model = data_source.tables[ProjectTeamPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.project_team_planning_period_systems = data_source.tables[ProjectTeamPlanningPeriodSystem].data_frame
        output_data.project_team_planning_period_system_time_sheets_by_date = data_source.tables[ProjectTeamPlanningPeriodSystemTimeSheetByDate].data_frame
        output_data.project_team_planning_period_system_time_sheets_by_date_model = data_source.tables[ProjectTeamPlanningPeriodSystemTimeSheetByDateModel].data_frame
        output_data.project_team_planning_periods = data_source.tables[ProjectTeamPlanningPeriod].data_frame
        output_data.project_team_positions = data_source.tables[ProjectTeamPosition].data_frame
        output_data.project_teams = data_source.tables[ProjectTeam].data_frame
        output_data.skills = data_source.tables[Skill].data_frame
        output_data.states = data_source.tables[State].data_frame
        output_data.state_categories = data_source.tables[StateCategory].data_frame
        output_data.systems = data_source.tables[System].data_frame
        output_data.system_change_requests = data_source.tables[SystemChangeRequest].data_frame
        output_data.system_change_request_analysis_time_sheets_by_date = data_source.tables[SystemChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.system_change_request_development_time_sheets_by_date = data_source.tables[SystemChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.system_change_request_testing_time_sheets_by_date = data_source.tables[SystemChangeRequestTestingTimeSheetByDate].data_frame
        output_data.system_change_request_time_sheets = data_source.tables[SystemChangeRequestTimeSheet].data_frame
        output_data.system_change_request_time_sheets_by_date = data_source.tables[SystemChangeRequestTimeSheetByDate].data_frame
        output_data.system_planning_periods = data_source.tables[SystemPlanningPeriod].data_frame
        output_data.system_planning_period_time_sheets_by_date = data_source.tables[SystemPlanningPeriodTimeSheetByDate].data_frame
        output_data.system_planning_period_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.system_planning_period_analysis_time_sheets_by_date = data_source.tables[SystemPlanningPeriodAnalysisTimeSheetByDate].data_frame
        output_data.system_planning_period_analysis_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodAnalysisTimeSheetByDateModel].data_frame
        output_data.system_planning_period_development_time_sheets_by_date = data_source.tables[SystemPlanningPeriodDevelopmentTimeSheetByDate].data_frame
        output_data.system_planning_period_development_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodDevelopmentTimeSheetByDateModel].data_frame
        output_data.system_planning_period_testing_time_sheets_by_date = data_source.tables[SystemPlanningPeriodTestingTimeSheetByDate].data_frame
        output_data.system_planning_period_testing_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodTestingTimeSheetByDateModel].data_frame
        output_data.task_analysis_time_sheets_by_date = data_source.tables[TaskAnalysisTimeSheetByDate].data_frame
        output_data.task_development_time_sheets_by_date = data_source.tables[TaskDevelopmentTimeSheetByDate].data_frame
        output_data.task_testing_time_sheets_by_date = data_source.tables[TaskTestingTimeSheetByDate].data_frame
        output_data.task_time_sheets = data_source.tables[TaskTimeSheet].data_frame
        output_data.task_time_sheets_by_date = data_source.tables[TaskTimeSheetByDate].data_frame
        output_data.tasks = data_source.tables[Task].data_frame

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

        calculate_companies_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_dedicated_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_project_teams_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        calculate_change_requests_actual_change_request_capacity_effort_and_queue_length(output_data=output_data)

        return output_data
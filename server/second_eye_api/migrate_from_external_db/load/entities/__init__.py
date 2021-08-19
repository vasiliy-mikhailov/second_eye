from .skills_loader import SkillsLoader
from .systems_loader import SystemsLoader
from .dedicated_teams_loader import DedicatedTeamsLoader
from .project_teams_loader import ProjectTeamsLoader
from .state_categories_loader import StateCategoriessLoader
from .states_loader import StatesLoader
from .change_requests_loader import ChangeRequestsLoader
from .system_change_requests_loader import SystemChangeRequestsLoader
from .tasks_loader import TasksLoader
from .function_component_kinds_loader import FunctionComponentKindsLoader
from .function_components_loader import FunctionComponentsLoader
from .persons_loader import PersonsLoader
from .dedicated_team_positions_loader import DedicatedTeamPositionsLoader
from .project_team_positions_loader import ProjectTeamPositionsLoader
from .dedicated_team_position_abilities_loader import DedicatedTeamPositionAbilitiesLoader
from .project_team_position_abilities_loader import ProjectTeamPositionAbilitiesLoader
from .task_time_sheets_loader import TaskTimeSheetsLoader
from .task_time_sheets_by_date_loader import TaskTimeSheetsByDateLoader
from .system_change_request_analysis_time_sheets_by_date_loader import SystemChangeRequestAnalysisTimeSheetsByDateLoader
from .system_change_requests_development_time_sheets_by_date_loader import SystemChangeRequestDevelopmentTimeSheetsByDateLoader
from .system_change_requests_testing_time_sheets_by_date_loader import SystemChangeRequestTestingTimeSheetsByDateLoader
from .system_change_request_time_sheets_by_date_loader import SystemChangeRequestTimeSheetsByDateLoader
from .change_request_analysis_time_sheets_by_date_loader import ChangeRequestAnalysisTimeSheetsByDateLoader
from .change_request_development_time_sheets_by_date_loader import ChangeRequestDevelopmentTimeSheetsByDateLoader
from .change_request_testing_time_sheets_by_date_loader import ChangeRequestTestingTimeSheetsByDateLoader
from .change_request_time_sheets_by_date_loader import ChangeRequestTimeSheetsByDateLoader
from .planning_periods_loader import PlanningPeriodsLoader
from .project_team_planning_periods_loader import ProjectTeamPlanningPeriodsLoader
from .dedicated_team_planning_period_loader import DedicatedTeamPlanningPeriodsLoader
from .dedicated_team_planning_period_time_sheets_by_date_loader import DedicatedTeamPlanningPeriodTimeSheetsByDateLoader
from .dedicated_team_planning_period_time_spent_with_value_and_without_value_by_date_loader import DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader
from .planning_period_time_sheets_by_date_loader import PlanningPeriodTimeSheetsByDateLoader
from .planning_period_time_spent_with_value_and_without_value_by_date_loader import PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader

class EntitiesLoader:
    def __init__(self, output_data, output_database):
        self.output_data = output_data
        self.output_database = output_database

    def load(self):
        output_data = self.output_data
        output_database = self.output_database

        skills_loader = SkillsLoader(skills=output_data.skills, output_database=output_database)
        skills_loader.load()

        systems_loader = SystemsLoader(systems=output_data.systems, output_database=output_database)
        systems_loader.load()

        dedicated_teams_loader = DedicatedTeamsLoader(dedicated_teams=output_data.dedicated_teams, output_database=output_database)
        dedicated_teams_loader.load()

        project_teams_loader = ProjectTeamsLoader(project_teams=output_data.project_teams, output_database=output_database)
        project_teams_loader.load()

        state_categories_loader = StateCategoriessLoader(state_categories=output_data.state_categories, output_database=output_database)
        state_categories_loader.load()

        states_loader = StatesLoader(states=output_data.states, output_database=output_database)
        states_loader.load()

        planning_periods_loader = PlanningPeriodsLoader(planning_periods=output_data.planning_periods, output_database=output_database)
        planning_periods_loader.load()

        dedicated_team_planning_periods_loader = DedicatedTeamPlanningPeriodsLoader(dedicated_team_planning_periods=output_data.dedicated_team_planning_periods, output_database=output_database)
        dedicated_team_planning_periods_loader.load()

        change_requests_loader = ChangeRequestsLoader(change_requests=output_data.change_requests, output_database=output_database)
        change_requests_loader.load()

        system_change_requests_loader = SystemChangeRequestsLoader(system_change_requests=output_data.system_change_requests, output_database=output_database)
        system_change_requests_loader.load()

        tasks_loader = TasksLoader(tasks=output_data.tasks, output_database=output_database)
        tasks_loader.load()

        function_component_kinds_loader = FunctionComponentKindsLoader(functionComponentKinds=output_data.function_component_kinds, output_database=output_database)
        function_component_kinds_loader.load()

        function_components_loader = FunctionComponentsLoader(function_components=output_data.function_components, output_database=output_database)
        function_components_loader.load()

        persons_loader = PersonsLoader(persons=output_data.persons, output_database=output_database)
        persons_loader.load()

        dedicated_team_positions_loader = DedicatedTeamPositionsLoader(dedicated_team_positions=output_data.dedicated_team_positions, output_database=output_database)
        dedicated_team_positions_loader.load()

        project_team_positions_loader = ProjectTeamPositionsLoader(project_team_positions=output_data.project_team_positions, output_database=output_database)
        project_team_positions_loader.load()

        dedicated_team_position_abilities_loader = DedicatedTeamPositionAbilitiesLoader(dedicated_team_position_abilities=output_data.dedicated_team_position_abilities, output_database=output_database)
        dedicated_team_position_abilities_loader.load()

        project_team_position_abilities_loader = ProjectTeamPositionAbilitiesLoader(project_team_position_abilities=output_data.project_team_position_abilities, output_database=output_database)
        project_team_position_abilities_loader.load()

        task_time_sheets_by_date_loader = TaskTimeSheetsByDateLoader(task_time_sheets_by_date=output_data.task_time_sheets_by_date, output_database=output_database)
        task_time_sheets_by_date_loader.load()

        system_change_request_analysis_time_sheets_by_date_loader = SystemChangeRequestAnalysisTimeSheetsByDateLoader(
            system_change_request_analysis_time_sheets_by_date=output_data.system_change_request_analysis_time_sheets_by_date,
            output_database=output_database
        )
        system_change_request_analysis_time_sheets_by_date_loader.load()

        system_change_request_development_time_sheets_by_date_loader = SystemChangeRequestDevelopmentTimeSheetsByDateLoader(
            system_change_request_development_time_sheets_by_date=output_data.system_change_request_development_time_sheets_by_date,
            output_database=output_database
        )
        system_change_request_development_time_sheets_by_date_loader.load()

        system_change_request_testing_time_sheets_by_date_loader = SystemChangeRequestTestingTimeSheetsByDateLoader(
            system_change_request_testing_time_sheets_by_date=output_data.system_change_request_testing_time_sheets_by_date,
            output_database=output_database
        )
        system_change_request_testing_time_sheets_by_date_loader.load()

        system_change_request_time_sheets_by_date_loader = SystemChangeRequestTimeSheetsByDateLoader(
            system_change_request_time_sheets_by_date=output_data.system_change_request_time_sheets_by_date,
            output_database=output_database
        )
        system_change_request_time_sheets_by_date_loader.load()

        change_request_analysis_time_sheets_by_date_loader = ChangeRequestAnalysisTimeSheetsByDateLoader(
            change_request_analysis_time_sheets_by_date=output_data.change_request_analysis_time_sheets_by_date,
            output_database=output_database
        )
        change_request_analysis_time_sheets_by_date_loader.load()

        change_request_development_time_sheets_by_date_loader = ChangeRequestDevelopmentTimeSheetsByDateLoader(
            change_request_development_time_sheets_by_date=output_data.change_request_development_time_sheets_by_date,
            output_database=output_database
        )
        change_request_development_time_sheets_by_date_loader.load()

        change_request_testing_time_sheets_by_date_loader = ChangeRequestTestingTimeSheetsByDateLoader(
            change_request_testing_time_sheets_by_date=output_data.change_request_testing_time_sheets_by_date,
            output_database=output_database
        )
        change_request_testing_time_sheets_by_date_loader.load()

        change_request_time_sheets_by_date_loader = ChangeRequestTimeSheetsByDateLoader(
            change_request_time_sheets_by_date=output_data.change_request_time_sheets_by_date,
            output_database=output_database
        )
        change_request_time_sheets_by_date_loader.load()

        # task_time_sheets_loader = TaskTimeSheetsLoader(task_time_sheets=output_data.task_time_sheets, output_database=output_database)
        # task_time_sheets_loader.load()

        project_team_planning_periods_loader = ProjectTeamPlanningPeriodsLoader(project_team_planning_periods=output_data.project_team_planning_periods, output_database=output_database)
        project_team_planning_periods_loader.load()

        dedicated_team_planning_period_time_sheets_by_date_loader = DedicatedTeamPlanningPeriodTimeSheetsByDateLoader(dedicated_team_planning_period_time_sheets_by_date=output_data.dedicated_team_planning_period_time_sheets_by_date, output_database=output_database)
        dedicated_team_planning_period_time_sheets_by_date_loader.load()

        dedicated_team_planning_period_time_spent_with_value_and_without_value_by_date_loader = DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader(
            dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date=output_data.dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date,
            output_database=output_database
        )
        dedicated_team_planning_period_time_spent_with_value_and_without_value_by_date_loader.load()

        planning_period_time_sheets_by_date_loader = PlanningPeriodTimeSheetsByDateLoader(planning_period_time_sheets_by_date=output_data.planning_period_time_sheets_by_date, output_database=output_database)
        planning_period_time_sheets_by_date_loader.load()

        planning_period_time_spent_with_value_and_without_value_by_date_loader = PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader(
            planning_period_time_spent_percent_with_value_and_without_value_by_date=output_data.planning_period_time_spent_percent_with_value_and_without_value_by_date,
            output_database=output_database
        )
        planning_period_time_spent_with_value_and_without_value_by_date_loader.load()
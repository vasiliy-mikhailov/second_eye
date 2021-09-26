from ..input_data import InputData
from ..utils import run_tasks_in_parallel
from .skills_extractor import SkillsExtractor
from .systems_extractor import SystemsExtractor
from .companies_extractor import CompaniesExtractor
from .dedicated_teams_extractor import DedicatedTeamsExtractor
from .project_teams_extractor import ProjectTeamsExtractor
from .state_categories_extractor import StateCategoriesExtractor
from .states_extractor import StatesExtractor
from .change_requests_extractor import ChangeRequestsExtractor
from .system_change_requests_extractor import SystemChangeRequestsExtractor
from .tasks_extractor import TasksExtractor
from .function_components_extractor import FunctionComponentsExtractor
from .function_component_kinds_extractor import FunctionComponentKindsExtractor
from .persons_extractor import PersonsExtractor
from .dedicated_team_positions_extractor import DedicatedTeamPositionsExtractor
from .project_team_positions_extractor import ProjectTeamPositionsExtractor
from .dedicated_team_position_abilities_extractor import DedicatedTeamPositionAbilitiesExtractor
from .project_team_position_abilities_extractor import ProjectTeamPositionAbilitiesExtractor
from .task_time_sheets_extractor import TaskTimeSheetsExtractor
from .planning_periods_extractor import PlaningPeriodsExtractor
from .system_change_requests_time_sheets_extractor import SystemChangeRequestsTimeSheetsExtractor

class Extractor:
    def __init__(self):
        pass

    def extract(self):
        input_data = InputData()

        skills_extractor = SkillsExtractor()
        systems_extractor = SystemsExtractor()
        companies_extractor = CompaniesExtractor()
        dedicated_teams_extractor = DedicatedTeamsExtractor()
        project_teams_extractor = ProjectTeamsExtractor()
        state_categories_extractor = StateCategoriesExtractor()
        states_extractor = StatesExtractor()
        change_requests_extractor = ChangeRequestsExtractor()
        system_change_requests_extractor = SystemChangeRequestsExtractor()
        tasks_extractor = TasksExtractor()
        function_component_kinds_extractor = FunctionComponentKindsExtractor()
        function_component_extractor = FunctionComponentsExtractor()
        persons_extractor = PersonsExtractor()
        dedicated_team_positions_extractor = DedicatedTeamPositionsExtractor()
        project_team_positions_extractor = ProjectTeamPositionsExtractor()
        dedicated_team_position_abilities_extractor = DedicatedTeamPositionAbilitiesExtractor()
        project_team_position_abilities_extractor = ProjectTeamPositionAbilitiesExtractor()
        task_time_sheets_extractor = TaskTimeSheetsExtractor()
        planning_periods_extractor = PlaningPeriodsExtractor()
        system_change_request_time_sheets_extractor = SystemChangeRequestsTimeSheetsExtractor()

        run_tasks_in_parallel([
            lambda: skills_extractor.extract(),
            lambda: systems_extractor.extract(),
            lambda: companies_extractor.extract(),
            lambda: dedicated_teams_extractor.extract(),
            lambda: project_teams_extractor.extract(),
            lambda: state_categories_extractor.extract(),
            lambda: states_extractor.extract(),
            lambda: change_requests_extractor.extract(),
            lambda: system_change_requests_extractor.extract(),
            lambda: tasks_extractor.extract(),
            lambda: function_component_kinds_extractor.extract(),
            lambda: function_component_extractor.extract(),
            lambda: persons_extractor.extract(),
            lambda: dedicated_team_positions_extractor.extract(),
            lambda: project_team_positions_extractor.extract(),
            lambda: dedicated_team_position_abilities_extractor.extract(),
            lambda: project_team_position_abilities_extractor.extract(),
            lambda: task_time_sheets_extractor.extract(),
            lambda: planning_periods_extractor.extract(),
            lambda: system_change_request_time_sheets_extractor.extract(),
        ])

        input_data.skills = skills_extractor.data

        input_data.systems = systems_extractor.data

        input_data.companies = companies_extractor.data

        input_data.dedicated_teams = dedicated_teams_extractor.data

        input_data.project_teams = project_teams_extractor.data

        input_data.state_categories = state_categories_extractor.data

        input_data.states = states_extractor.data

        input_data.change_requests = change_requests_extractor.data

        input_data.system_change_requests = system_change_requests_extractor.data

        input_data.tasks = tasks_extractor.data

        input_data.function_component_kinds = function_component_kinds_extractor.data

        input_data.function_components = function_component_extractor.data

        input_data.persons = persons_extractor.data

        input_data.dedicated_team_positions = dedicated_team_positions_extractor.data

        input_data.project_team_positions = project_team_positions_extractor.data

        input_data.dedicated_team_position_abilities = dedicated_team_position_abilities_extractor.data

        input_data.project_team_position_abilities = project_team_position_abilities_extractor.data

        input_data.task_time_sheets = task_time_sheets_extractor.data

        input_data.planning_periods = planning_periods_extractor.data

        input_data.system_change_request_time_sheets = system_change_request_time_sheets_extractor.data

        return input_data
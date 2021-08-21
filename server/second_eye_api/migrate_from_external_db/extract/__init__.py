from second_eye_api.migrate_from_external_db.input_data import InputData
from second_eye_api.migrate_from_external_db.extract.utils import run_tasks_in_parallel
from .entities.skills_extractor import SkillsExtractor
from .entities.systems_extractor import SystemsExtractor
from .entities.companies_extractor import CompaniesExtractor
from .entities.dedicated_teams_extractor import DedicatedTeamsExtractor
from .entities.project_teams_extractor import ProjectTeamsExtractor
from .entities.state_categories_extractor import StateCategoriesExtractor
from .entities.states_extractor import StatesExtractor
from .entities.change_requests_extractor import ChangeRequestsExtractor
from .entities.system_change_requests_extractor import SystemChangeRequestsExtractor
from .entities.tasks_extractor import TasksExtractor
from .entities.function_components_extractor import FunctionComponentsExtractor
from .entities.function_component_kinds_extractor import FunctionComponentKindsExtractor
from .entities.persons_extractor import PersonsExtractor
from .entities.dedicated_team_positions_extractor import DedicatedTeamPositionsExtractor
from .entities.project_team_positions_extractor import ProjectTeamPositionsExtractor
from .entities.dedicated_team_position_abilities_extractor import DedicatedTeamPositionAbilitiesExtractor
from .entities.project_team_position_abilities_extractor import ProjectTeamPositionAbilitiesExtractor
from .entities.task_time_sheets_extractor import TaskTimeSheetsExtractor
from .entities.planning_periods_extractor import PlaningPeriodsExtractor

class Extractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        input_data = InputData()

        skills_extractor = SkillsExtractor()
        systems_extractor = SystemsExtractor(get_connection=get_connection)
        companies_extractor = CompaniesExtractor()
        dedicated_teams_extractor = DedicatedTeamsExtractor(get_connection=get_connection)
        project_teams_extractor = ProjectTeamsExtractor(get_connection=get_connection)
        state_categories_extractor = StateCategoriesExtractor()
        states_extractor = StatesExtractor(get_connection=get_connection)
        change_requests_extractor = ChangeRequestsExtractor(get_connection=get_connection)
        system_change_requests_extractor = SystemChangeRequestsExtractor(get_connection=get_connection)
        tasks_extractor = TasksExtractor(get_connection=get_connection)
        function_component_kinds_extractor = FunctionComponentKindsExtractor()
        function_component_extractor = FunctionComponentsExtractor(get_connection=get_connection)
        persons_extractor = PersonsExtractor(get_connection=get_connection)
        dedicated_team_positions_extractor = DedicatedTeamPositionsExtractor(get_connection=get_connection)
        project_team_positions_extractor = ProjectTeamPositionsExtractor(get_connection=get_connection)
        dedicated_team_position_abilities_extractor = DedicatedTeamPositionAbilitiesExtractor(get_connection=get_connection)
        project_team_position_abilities_extractor = ProjectTeamPositionAbilitiesExtractor(get_connection=get_connection)
        task_time_sheets_extractor = TaskTimeSheetsExtractor(get_connection=get_connection)
        planning_periods_extractor = PlaningPeriodsExtractor(get_connection=get_connection)

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

        return input_data
from ..input_data import InputData
from ..utils import run_tasks_in_parallel

from .change_requests_extractor import ChangeRequestsExtractor
from .companies_extractor import CompaniesExtractor
from .dedicated_team_position_abilities_extractor import DedicatedTeamPositionAbilitiesExtractor
from .dedicated_team_positions_extractor import DedicatedTeamPositionsExtractor
from .dedicated_teams_extractor import DedicatedTeamsExtractor
from .epics_extractor import EpicsExtractor
from .function_component_kinds_extractor import FunctionComponentKindsExtractor
from .function_components_extractor import FunctionComponentsExtractor
from .incidents_extractor import IncidentsExtractor
from .incident_sub_task_time_sheets_extractor import IncidentSubTaskTimeSheetsExtractor
from .incident_sub_tasks_extractor import IncidentSubTasksExtractor
from .incident_time_sheets_extractor import IncidentTimeSheetsExtractor
from .non_project_activities_extractor import NonProjectActivitiesExtractor
from .non_project_activity_time_sheets_extractor import NonProjectActivityTimeSheetsExtractor
from .persons_extractor import PersonsExtractor
from .planning_periods_extractor import PlaningPeriodsExtractor
from .project_team_position_abilities_extractor import ProjectTeamPositionAbilitiesExtractor
from .project_team_positions_extractor import ProjectTeamPositionsExtractor
from .project_teams_extractor import ProjectTeamsExtractor
from .quarters_extractor import QuartersExtractor
from .skills_extractor import SkillsExtractor
from .state_categories_extractor import StateCategoriesExtractor
from .states_extractor import StatesExtractor
from .system_change_requests_extractor import SystemChangeRequestsExtractor
from .system_change_requests_time_sheets_extractor import SystemChangeRequestsTimeSheetsExtractor
from .systems_extractor import SystemsExtractor
from .task_time_sheets_extractor import TaskTimeSheetsExtractor
from .tasks_extractor import TasksExtractor

class Extractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        input_data = InputData()

        change_requests_extractor = ChangeRequestsExtractor(get_connection=get_connection)
        companies_extractor = CompaniesExtractor()
        dedicated_team_position_abilities_extractor = DedicatedTeamPositionAbilitiesExtractor(get_connection=get_connection)
        dedicated_team_positions_extractor = DedicatedTeamPositionsExtractor(get_connection=get_connection)
        dedicated_teams_extractor = DedicatedTeamsExtractor(get_connection=get_connection)
        epics_extractor = EpicsExtractor(get_connection=get_connection)
        function_component_extractor = FunctionComponentsExtractor(get_connection=get_connection)
        function_component_kinds_extractor = FunctionComponentKindsExtractor()
        incident_sub_task_time_sheets_extractor = IncidentSubTaskTimeSheetsExtractor(get_connection=get_connection)
        incident_sub_tasks_extractor = IncidentSubTasksExtractor(get_connection=get_connection)
        incident_time_sheets_extractor = IncidentTimeSheetsExtractor(get_connection=get_connection)
        incidents_extractor = IncidentsExtractor(get_connection=get_connection)
        non_project_activities_extractor = NonProjectActivitiesExtractor(get_connection=get_connection)
        non_project_activity_time_sheets_extractor = NonProjectActivityTimeSheetsExtractor(get_connection=get_connection)
        persons_extractor = PersonsExtractor(get_connection=get_connection)
        planning_periods_extractor = PlaningPeriodsExtractor(get_connection=get_connection)
        project_team_position_abilities_extractor = ProjectTeamPositionAbilitiesExtractor(get_connection=get_connection)
        project_team_positions_extractor = ProjectTeamPositionsExtractor(get_connection=get_connection)
        project_teams_extractor = ProjectTeamsExtractor(get_connection=get_connection)
        quarters_extractor = QuartersExtractor()
        skills_extractor = SkillsExtractor()
        state_categories_extractor = StateCategoriesExtractor()
        states_extractor = StatesExtractor(get_connection=get_connection)
        system_change_request_time_sheets_extractor = SystemChangeRequestsTimeSheetsExtractor(get_connection=get_connection)
        system_change_requests_extractor = SystemChangeRequestsExtractor(get_connection=get_connection)
        systems_extractor = SystemsExtractor(get_connection=get_connection)
        task_time_sheets_extractor = TaskTimeSheetsExtractor(get_connection=get_connection)
        tasks_extractor = TasksExtractor(get_connection=get_connection)

        run_tasks_in_parallel([
            lambda: change_requests_extractor.extract(),
            lambda: companies_extractor.extract(),
            lambda: dedicated_team_position_abilities_extractor.extract(),
            lambda: dedicated_team_positions_extractor.extract(),
            lambda: dedicated_teams_extractor.extract(),
            lambda: epics_extractor.extract(),
            lambda: function_component_extractor.extract(),
            lambda: function_component_kinds_extractor.extract(),
            lambda: incident_sub_task_time_sheets_extractor.extract(),
            lambda: incident_sub_tasks_extractor.extract(),
            lambda: incident_time_sheets_extractor.extract(),
            lambda: incidents_extractor.extract(),
            lambda: non_project_activities_extractor.extract(),
            lambda: non_project_activity_time_sheets_extractor.extract(),
            lambda: persons_extractor.extract(),
            lambda: planning_periods_extractor.extract(),
            lambda: project_team_position_abilities_extractor.extract(),
            lambda: project_team_positions_extractor.extract(),
            lambda: project_teams_extractor.extract(),
            lambda: quarters_extractor.extract(),
            lambda: skills_extractor.extract(),
            lambda: state_categories_extractor.extract(),
            lambda: states_extractor.extract(),
            lambda: system_change_request_time_sheets_extractor.extract(),
            lambda: system_change_requests_extractor.extract(),
            lambda: systems_extractor.extract(),
            lambda: task_time_sheets_extractor.extract(),
            lambda: tasks_extractor.extract(),
        ])

        input_data.change_requests = change_requests_extractor.data
        input_data.companies = companies_extractor.data
        input_data.dedicated_team_position_abilities = dedicated_team_position_abilities_extractor.data
        input_data.dedicated_team_positions = dedicated_team_positions_extractor.data
        input_data.dedicated_teams = dedicated_teams_extractor.data
        input_data.epics = epics_extractor.data
        input_data.function_component_kinds = function_component_kinds_extractor.data
        input_data.function_components = function_component_extractor.data
        input_data.incident_sub_task_time_sheets = incident_sub_task_time_sheets_extractor.data
        input_data.incident_sub_tasks = incident_sub_tasks_extractor.data
        input_data.incident_time_sheets = incident_time_sheets_extractor.data
        input_data.incidents = incidents_extractor.data
        input_data.non_project_activities = non_project_activities_extractor.data
        input_data.non_project_activity_time_sheets = non_project_activity_time_sheets_extractor.data
        input_data.persons = persons_extractor.data
        input_data.planning_periods = planning_periods_extractor.data
        input_data.project_team_position_abilities = project_team_position_abilities_extractor.data
        input_data.project_team_positions = project_team_positions_extractor.data
        input_data.project_teams = project_teams_extractor.data
        input_data.quarters = quarters_extractor.data
        input_data.skills = skills_extractor.data
        input_data.state_categories = state_categories_extractor.data
        input_data.states = states_extractor.data
        input_data.system_change_request_time_sheets = system_change_request_time_sheets_extractor.data
        input_data.system_change_requests = system_change_requests_extractor.data
        input_data.systems = systems_extractor.data
        input_data.task_time_sheets = task_time_sheets_extractor.data
        input_data.tasks = tasks_extractor.data

        return input_data
from ..input_data import InputData
from ..utils import run_tasks_in_parallel

from .change_requests_creator import ChangeRequestsCreator
from .companies_creator import CompaniesCreator
from .dedicated_team_position_abilities_creator import DedicatedTeamPositionAbilitiesCreator
from .dedicated_team_positions_creator import DedicatedTeamPositionsCreator
from .dedicated_teams_creator import DedicatedTeamsCreator
from .epics_creator import EpicsCreator
from .function_component_kinds_creator import FunctionComponentKindsCreator
from .function_components_creator import FunctionComponentsCreator
from .incidents_creator import IncidentsCreator
from .incident_sub_task_time_sheets_creator import IncidentSubTaskTimeSheetsCreator
from .incident_sub_tasks_creator import IncidentsSubTasksCreator
from .incident_time_sheets_creator import IncidentTimeSheetsCreator
from .management_time_sheets_creator import ManagementTimeSheetsCreator
from .non_project_activities_creator import NonProjectActivitiesCreator
from .non_project_activity_time_sheets_creator import NonProjectActivityTimeSheetsCreator
from .persons_creator import PersonsCreator
from .planning_periods_creator import PlaningPeriodsCreator
from .project_team_position_abilities_creator import ProjectTeamPositionAbilitiesCreator
from .project_team_positions_creator import ProjectTeamPositionsCreator
from .project_teams_creator import ProjectTeamsCreator
from .quarters_creator import QuartersCreator
from .skills_creator import SkillsCreator
from .state_categories_creator import StateCategoriesCreator
from .states_creator import StatesCreator
from .system_change_requests_creator import SystemChangeRequestsCreator
from .systems_creator import SystemsCreator
from .task_time_sheets_creator import TaskTimeSheetsCreator
from .tasks_creator import TasksCreator

class TestDataCreator:
    def __init__(self):
        self.change_requests_creator = ChangeRequestsCreator()
        self.companies_creator = CompaniesCreator()
        self.dedicated_team_position_abilities_creator = DedicatedTeamPositionAbilitiesCreator()
        self.dedicated_team_positions_creator = DedicatedTeamPositionsCreator()
        self.dedicated_teams_creator = DedicatedTeamsCreator()
        self.epics_creator = EpicsCreator()
        self.function_component_creator = FunctionComponentsCreator()
        self.function_component_kinds_creator = FunctionComponentKindsCreator()
        self.incidents_creator = IncidentsCreator()
        self.incident_sub_task_time_sheets_creator = IncidentSubTaskTimeSheetsCreator()
        self.incident_sub_tasks_creator = IncidentsSubTasksCreator()
        self.incident_time_sheets_creator = IncidentTimeSheetsCreator()
        self.management_time_sheets_creator = ManagementTimeSheetsCreator()
        self.non_project_activities_creator = NonProjectActivitiesCreator()
        self.non_project_activity_time_sheets_creator = NonProjectActivityTimeSheetsCreator()
        self.persons_creator = PersonsCreator()
        self.planning_periods_creator = PlaningPeriodsCreator()
        self.project_team_position_abilities_creator = ProjectTeamPositionAbilitiesCreator()
        self.project_team_positions_creator = ProjectTeamPositionsCreator()
        self.project_teams_creator = ProjectTeamsCreator()
        self.quarters_creator = QuartersCreator()
        self.skills_creator = SkillsCreator()
        self.state_categories_creator = StateCategoriesCreator()
        self.states_creator = StatesCreator()
        self.system_change_requests_creator = SystemChangeRequestsCreator()
        self.systems_creator = SystemsCreator()
        self.task_time_sheets_creator = TaskTimeSheetsCreator()
        self.tasks_creator = TasksCreator()

    def create_change_request(self, key, name, project_team_id=-1, state_id=-1, resolution_date=None, quarter_key="-1", analysis_express_estimate = 0, development_express_estimate = 0, testing_express_estimate = 0):
        change_requests_creator = self.change_requests_creator

        return change_requests_creator.create_change_request(
            key=key,
            name=name,
            project_team_id=project_team_id,
            state_id=state_id,
            resolution_date=resolution_date,
            quarter_key=quarter_key,
            analysis_express_estimate=analysis_express_estimate,
            development_express_estimate=development_express_estimate,
            testing_express_estimate=testing_express_estimate
        )

    def create_company(self, name, id=None):
        companies_creator = self.companies_creator

        return companies_creator.create_company(name=name, id=id)

    def create_dedicated_team(self, name, company_id):
        dedicated_teams_creator = self.dedicated_teams_creator

        return dedicated_teams_creator.create_dedicated_team(name=name, company_id=company_id)

    def create_epic(self, key, name):
        epics_creator = self.epics_creator

        return epics_creator.create_epic(key=key, name=name)

    def create_function_component(self, task_id, kind_id, name, count):
        function_components_creator = self.function_component_creator

        return function_components_creator.create_function_component(task_id=task_id, kind_id=kind_id, name=name, count=count)

    def create_incident_sub_task(self, key, name, incident_id, skill_id):
        incident_subtasks_creator = self.incident_sub_tasks_creator

        return incident_subtasks_creator.create_incident_sub_task(key=key, name=name, incident_id=incident_id, skill_id=skill_id)

    def create_incident_sub_task_time_sheet(self, incident_sub_task_id, date, time_spent, person_key):
        incident_sub_task_time_sheets_creator = self.incident_sub_task_time_sheets_creator

        return incident_sub_task_time_sheets_creator.create_incident_sub_task_time_sheet(incident_sub_task_id=incident_sub_task_id, date=date, time_spent=time_spent, person_key=person_key)

    def create_incident_time_sheet(self, incident_id, date, time_spent, person_key):
        incident_time_sheets_creator = self.incident_time_sheets_creator

        return incident_time_sheets_creator.create_incident_time_sheet(incident_id=incident_id, date=date, time_spent=time_spent, person_key=person_key)

    def create_non_project_activity(self, key, name, company_id):
        non_project_activities_creator = self.non_project_activities_creator

        return non_project_activities_creator.create_non_project_activity(key=key, name=name, company_id=company_id)

    def create_non_project_activity_time_sheet(self, non_project_activity_id, date, time_spent, person_key):
        non_project_activity_time_sheets_creator = self.non_project_activity_time_sheets_creator

        return non_project_activity_time_sheets_creator.create_non_project_activity_time_sheet(non_project_activity_id=non_project_activity_id, date=date, time_spent=time_spent, person_key=person_key)

    def create_management_time_sheet(self, system_change_request_id, date, time_spent, person_key):
        management_time_sheets_creator = self.management_time_sheets_creator

        return management_time_sheets_creator.create_management_time_sheet(system_change_request_id=system_change_request_id, date=date, time_spent=time_spent, person_key=person_key)

    def create_person(self, name):
        persons_creator = self.persons_creator

        return persons_creator.create_person(name=name)

    def create_planning_period(self, id):
        planning_periods_creator = self.planning_periods_creator

        return planning_periods_creator.create_planning_period(id=id)

    def create_project_team(self, name, dedicated_team_id, project_manager_key="-1"):
        project_teams_creator = self.project_teams_creator

        return project_teams_creator.create_project_team(name=name, dedicated_team_id=dedicated_team_id, project_manager_key=project_manager_key)

    def create_system_change_request(self, key, name, change_request_id, system_id):
        system_change_requests_creator = self.system_change_requests_creator

        return system_change_requests_creator.create_system_change_request(key=key, name=name, change_request_id=change_request_id, system_id=system_id)

    def create_quarter(self, name, year, quarter_number):
        quarters_creator = self.quarters_creator

        return quarters_creator.create_quarter(name=name, year=year, quarter_number=quarter_number)

    def create_system(self, name):
        systems_creator = self.systems_creator

        return systems_creator.create_system(name=name)

    def create_task(self, key, name, system_change_request_id, skill_id):
        tasks_creator = self.tasks_creator

        return tasks_creator.create_task(key=key, name=name, system_change_request_id=system_change_request_id, skill_id=skill_id)

    def create_task_time_sheet(self, task_id, date, time_spent, person_key):
        task_time_sheets_creator = self.task_time_sheets_creator

        return task_time_sheets_creator.create_task_time_sheet(task_id=task_id, date=date, time_spent=time_spent, person_key=person_key)

    def create_incident(self, key, name, system_id=-1, project_team_id=-1, state_id=-1, resolution_date=None):
        incidents_creator = self.incidents_creator

        return incidents_creator.create_incident(key=key, name=name, system_id=system_id, project_team_id=project_team_id, state_id=state_id, resolution_date=resolution_date)

    def extract(self):
        input_data = InputData()

        change_requests_creator = self.change_requests_creator
        companies_creator = self.companies_creator
        dedicated_team_position_abilities_creator = self.dedicated_team_position_abilities_creator
        dedicated_team_positions_creator = self.dedicated_team_positions_creator
        dedicated_teams_creator = self.dedicated_teams_creator
        epics_creator = self.epics_creator
        function_component_creator = self.function_component_creator
        function_component_kinds_creator = self.function_component_kinds_creator
        incidents_creator = self.incidents_creator
        incident_sub_task_time_sheets_creator = self.incident_sub_task_time_sheets_creator
        incident_sub_tasks_creator = self.incident_sub_tasks_creator
        incident_time_sheets_creator = self.incident_time_sheets_creator
        non_project_activities_creator = self.non_project_activities_creator
        non_project_activity_time_sheets_creator = self.non_project_activity_time_sheets_creator
        persons_creator = self.persons_creator
        planning_periods_creator = self.planning_periods_creator
        project_team_position_abilities_creator = self.project_team_position_abilities_creator
        project_team_positions_creator= self.project_team_positions_creator
        project_teams_creator = self.project_teams_creator
        quarters_creator = self.quarters_creator
        skills_creator= self.skills_creator
        state_categories_creator = self.state_categories_creator
        states_creator = self.states_creator
        system_change_request_time_sheets_creator = self.management_time_sheets_creator
        system_change_requests_creator = self.system_change_requests_creator
        systems_creator = self.systems_creator
        task_time_sheets_creator = self.task_time_sheets_creator
        tasks_creator = self.tasks_creator

        run_tasks_in_parallel([
            lambda: change_requests_creator.extract(),
            lambda: companies_creator.extract(),
            lambda: dedicated_team_position_abilities_creator.extract(),
            lambda: dedicated_team_positions_creator.extract(),
            lambda: dedicated_teams_creator.extract(),
            lambda: epics_creator.extract(),
            lambda: function_component_creator.extract(),
            lambda: function_component_kinds_creator.extract(),
            lambda: incidents_creator.extract(),
            lambda: incident_sub_task_time_sheets_creator.extract(),
            lambda: incident_sub_tasks_creator.extract(),
            lambda: incident_time_sheets_creator.extract(),
            lambda: non_project_activities_creator.extract(),
            lambda: non_project_activity_time_sheets_creator.extract(),
            lambda: persons_creator.extract(),
            lambda: planning_periods_creator.extract(),
            lambda: project_team_position_abilities_creator.extract(),
            lambda: project_team_positions_creator.extract(),
            lambda: project_teams_creator.extract(),
            lambda: quarters_creator.extract(),
            lambda: skills_creator.extract(),
            lambda: state_categories_creator.extract(),
            lambda: states_creator.extract(),
            lambda: system_change_request_time_sheets_creator.extract(),
            lambda: system_change_requests_creator.extract(),
            lambda: systems_creator.extract(),
            lambda: task_time_sheets_creator.extract(),
            lambda: tasks_creator.extract(),
        ])

        input_data.change_requests = change_requests_creator.data
        input_data.companies = companies_creator.data
        input_data.dedicated_teams = dedicated_teams_creator.data
        input_data.dedicated_team_position_abilities = dedicated_team_position_abilities_creator.data
        input_data.dedicated_team_positions = dedicated_team_positions_creator.data
        input_data.epics = epics_creator.data
        input_data.function_component_kinds = function_component_kinds_creator.data
        input_data.function_components = function_component_creator.data
        input_data.incidents = incidents_creator.data
        input_data.incident_sub_task_time_sheets = incident_sub_task_time_sheets_creator.data
        input_data.incident_sub_tasks = incident_sub_tasks_creator.data
        input_data.incident_time_sheets = incident_time_sheets_creator.data
        input_data.non_project_activities = non_project_activities_creator.data
        input_data.non_project_activity_time_sheets = non_project_activity_time_sheets_creator.data
        input_data.planning_periods = planning_periods_creator.data
        input_data.project_team_position_abilities = project_team_position_abilities_creator.data
        input_data.project_team_positions = project_team_positions_creator.data
        input_data.project_teams = project_teams_creator.data
        input_data.persons = persons_creator.data
        input_data.quarters = quarters_creator.data
        input_data.skills = skills_creator.data
        input_data.state_categories = state_categories_creator.data
        input_data.states = states_creator.data
        input_data.system_change_request_time_sheets = system_change_request_time_sheets_creator.data
        input_data.system_change_requests = system_change_requests_creator.data
        input_data.systems = systems_creator.data
        input_data.task_time_sheets = task_time_sheets_creator.data
        input_data.tasks = tasks_creator.data

        return input_data
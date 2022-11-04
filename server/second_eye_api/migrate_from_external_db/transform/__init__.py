from .change_request import *
from .company import *
from .dedicated_team import *
from .dedicated_team_planning_period import *
from .dedicated_team_planning_period_system import *
from .dedicated_team_quarter import *
from .dedicated_team_quarter_system import *
from .epic import *
from .epic_system import *
from .function_component import *
from .incident import *
from .incident_sub_task import *
from .issue import *
from .non_project_activity import *
from .person import *
from .person_change_request import *
from .person_dedicated_team import *
from .person_dedicated_team_planning_period import *
from .person_epic import *
from .person_incident import *
from .person_incident_month import *
from .person_month import *
from .person_non_project_activity import *
from .person_non_project_activity_month import *
from .person_planning_period import *
from .person_project_team import *
from .person_project_team_month import *
from .person_project_team_planning_period import *
from .person_system import *
from .person_system_change_request import *
from .person_system_change_request_month import *
from .person_task import *
from .person_task_month import *
from .planning_period import *
from .project_manager import *
from .project_manager_month import *
from .project_team import *
from .project_team_current_quarter import *
from .project_team_planning_period import *
from .project_team_planning_period_system import *
from .project_team_quarter import *
from .project_team_quarter_system import *
from .quarter import *
from .skill import *
from .state import *
from .system import *
from .system_change_request import *
from .system_change_requests_transform import *
from .system_planning_period import *
from .task import *
from .tasks_transform import *
from .time_sheet import *
from .time_sheet_by_date_model import *
from .utils import *
from .work_item import *
from ..output_data import OutputData

class Transformer:
    def __init__(self, input_data):
        self.input_data = input_data

    def transform(self):
        input_data = self.input_data

        change_request = ChangeRequest(data_frame=input_data.change_requests)
        change_request_analysis_time_sheet_by_date = ChangeRequestAnalysisTimeSheetByDate()
        change_request_calculated_date_after_quarter_end_issue = ChangeRequestCalculatedDateAfterQuarterEndIssue()
        change_request_development_time_sheet_by_date = ChangeRequestDevelopmentTimeSheetByDate()
        change_request_testing_time_sheet_by_date = ChangeRequestTestingTimeSheetByDate()
        change_request_time_sheet_by_date = ChangeRequestTimeSheetByDate()
        change_request_time_sheet_by_date_model = ChangeRequestTimeSheetByDateModel()
        change_request_time_spent = ChangeRequestTimeSpent()
        change_request_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter = ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter()
        companies = Company(data_frame=input_data.companies)
        company_time_spent = CompanyTimeSpent()
        company_time_sheet_by_date = CompanyTimeSheetByDate()
        company_time_sheet_by_date_model = CompanyTimeSheetByDateModel()
        dedicated_team = DedicatedTeam(data_frame=input_data.dedicated_teams)
        dedicated_team_dedicated_team_planning_period_position = DedicatedTeamDedicatedTeamPlanningPeriodPosition()
        dedicated_team_planning_period = DedicatedTeamPlanningPeriod()
        dedicated_team_planning_period_position_person_time_spent = DedicatedTeamPlanningPeriodPositionPersonTimeSpent()
        dedicated_team_planning_period_system = DedicatedTeamPlanningPeriodSystem()
        dedicated_team_planning_period_system_time_sheet_by_date = DedicatedTeamPlanningPeriodSystemTimeSheetByDate()
        dedicated_team_planning_period_system_time_sheet_by_date_model = DedicatedTeamPlanningPeriodSystemTimeSheetByDateModel()
        dedicated_team_planning_period_time_sheet_by_date = DedicatedTeamPlanningPeriodTimeSheetByDate()
        dedicated_team_planning_period_time_sheet_by_date_model = DedicatedTeamPlanningPeriodTimeSheetByDateModel()
        dedicated_team_planning_period_time_spent_previous_28_days = DedicatedTeamPlanningPeriodTimeSpentChronon()
        dedicated_team_position = DedicatedTeamPosition(data_frame=input_data.dedicated_team_positions)
        dedicated_team_quarter = DedicatedTeamQuarter()
        dedicated_team_quarter_system = DedicatedTeamQuarterSystem()
        dedicated_team_quarter_system_time_sheet_by_date = DedicatedTeamQuarterSystemTimeSheetByDate()
        dedicated_team_quarter_system_time_sheet_by_date_model = DedicatedTeamQuarterSystemTimeSheetByDateModel()
        dedicated_team_quarter_time_sheet_by_date = DedicatedTeamQuarterTimeSheetByDate()
        dedicated_team_quarter_time_sheet_by_date_model = DedicatedTeamQuarterTimeSheetByDateModel()
        dedicated_team_time_sheet_by_date = DedicatedTeamTimeSheetByDate()
        dedicated_team_time_sheet_by_date_model = DedicatedTeamTimeSheetByDateModel()
        dedicated_team_time_spent = DedicatedTeamTimeSpent()
        epic = Epic(data_frame=input_data.epics)
        epic_analysis_time_sheet_by_date = EpicAnalysisTimeSheetByDate()
        epic_development_time_sheet_by_date = EpicDevelopmentTimeSheetByDate()
        epic_system = EpicSystem()
        epic_system_time_sheet_by_date = EpicSystemTimeSheetByDate()
        epic_system_time_sheet_by_date_model = EpicSystemTimeSheetByDateModel()
        epic_testing_time_sheet_by_date = EpicTestingTimeSheetByDate()
        epic_time_sheet_by_date = EpicTimeSheetByDate()
        epic_time_sheet_by_date_model = EpicTimeSheetByDateModel()
        function_component = FunctionComponent(data_frame=input_data.function_components)
        function_component_kind = FunctionComponentKind(data_frame=input_data.function_component_kinds)
        incident = Incident(data_frame=input_data.incidents)
        incident_no_incident_sub_task_aggregation_time_sheet = IncidentNoIncidentSubTaskAggregationTimeSheet(data_frame=input_data.incident_time_sheets)
        incident_sub_task = IncidentSubTask(data_frame=input_data.incident_sub_tasks)
        incident_sub_task_time_sheet = IncidentSubTaskTimeSheet(data_frame=input_data.incident_sub_task_time_sheets)
        incident_time_sheet = IncidentTimeSheet()
        incident_time_sheet_by_date = IncidentTimeSheetByDate()
        incident_time_spent = IncidentTimeSpent()
        management_time_sheet = ManagementTimeSheet(data_frame=input_data.system_change_request_time_sheets)
        non_project_activity = NonProjectActivity(data_frame=input_data.non_project_activities)
        non_project_activity_time_sheets = NonProjectActivityTimeSheet(data_frame=input_data.non_project_activity_time_sheets)
        project_team_position_person_plan_fact_issue = ProjectTeamPositionPersonPlanFactIssue()
        person = Person(data_frame=input_data.persons)
        person_change_request_time_spent = PersonChangeRequestTimeSpent()
        person_dedicated_team_time_spent = PersonDedicatedTeamTimeSpent()
        person_dedicated_team_planning_period = PersonDedicatedTeamPlanningPeriod()
        person_epic = PersonEpic()
        person_incident_month_time_spent = PersonIncidentMonthTimeSpent()
        person_incident_time_spent = PersonIncidentTimeSpent()
        person_month = PersonMonthTimeSpent()
        person_non_project_activity = PersonNonProjectActivityTimeSpent()
        person_non_project_activity_month = PersonNonProjectActivityMonthTimeSpent()
        person_planning_period = PersonPlanningPeriodTimeSpent()
        person_project_team_month = PersonProjectTeamMonth()
        person_project_team_persons_last_180_days_time_sheet = PersonProjectTeamPersonsLast180DaysTimeSheet()
        person_project_team_planning_period = PersonProjectTeamPlanningPeriodTimeSpent()
        person_project_team_time_spent = PersonProjectTeamTimeSpent()
        person_system_change_request = PersonSystemChangeRequestTimeSpent()
        person_system_change_request_month_time_spent = PersonSystemChangeRequestMonthTimeSpent()
        person_system_change_request_time_sheet_by_date = PersonSystemChangeRequestTimeSheetByDate()
        person_system = PersonSystem()
        person_task_month_time_spent = PersonTaskMonthTimeSpent()
        person_task_time_sheet_by_date = PersonTaskTimeSheetByDate()
        person_time_sheet_by_date = PersonTimeSheetByDate()
        person_task_time_spent = PersonTaskTimeSpent()
        persons_with_time_spent_for_change_requests_in_current_quarter_while_change_requests_not_in_current_quarter = PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter()
        planning_period = PlanningPeriod(data_frame=input_data.planning_periods)
        planning_period_time_sheet_by_date = PlanningPeriodTimeSheetByDate()
        planning_period_time_sheet_by_date_model = PlanningPeriodTimeSheetByDateModel()
        planning_period_time_spent = PlanningPeriodTimeSpent()
        project_manager = ProjectManager()
        project_manager_month = ProjectManagerMonth()
        project_team = ProjectTeam(data_frame=input_data.project_teams)
        project_team_planning_period = ProjectTeamPlanningPeriod()
        project_team_planning_period_system = ProjectTeamPlanningPeriodSystem()
        project_team_planning_period_system_time_sheet_by_date = ProjectTeamPlanningPeriodSystemTimeSheetByDate()
        project_team_planning_period_system_time_sheet_by_date_model = ProjectTeamPlanningPeriodSystemTimeSheetByDateModel()
        project_team_planning_period_time_sheet_by_date = ProjectTeamPlanningPeriodTimeSheetByDate()
        project_team_planning_period_time_sheet_by_date_model = ProjectTeamPlanningPeriodTimeSheetByDateModel()
        project_team_current_quarter = ProjectTeamCurrentQuarter()
        project_team_quarter = ProjectTeamQuarter()
        project_team_quarter_system = ProjectTeamQuarterSystem()
        project_team_quarter_system_time_sheet_by_date = ProjectTeamQuarterSystemTimeSheetByDate()
        project_team_quarter_system_time_sheet_by_date_model = ProjectTeamQuarterSystemTimeSheetByDateModel()
        project_team_quarter_time_sheet_by_date = ProjectTeamQuarterTimeSheetByDate()
        project_team_quarter_time_sheet_by_date_model = ProjectTeamQuarterTimeSheetByDateModel()
        project_team_position = ProjectTeamPosition(data_frame=input_data.project_team_positions)
        project_team_position_person_time_spent = ProjectTeamPositionPersonTimeSpent()
        project_team_position_person_time_spent_chronon = ProjectTeamPositionPersonTimeSpentChronon()
        project_team_project_team_planning_period_position = ProjectTeamProjectTeamPlanningPeriodPosition()
        project_team_time_sheet_by_date = ProjectTeamTimeSheetByDate()
        project_team_time_sheet_by_date_model = ProjectTeamTimeSheetByDateModel()
        project_team_time_sheet_by_month = ProjectTeamTimeSheetByMonth()
        project_team_analysis_time_sheet_by_month = ProjectTeamAnalysisTimeSheetByMonth()
        project_team_development_time_sheet_by_month = ProjectTeamDevelopmentTimeSheetByMonth()
        project_team_testing_time_sheet_by_month = ProjectTeamTestingTimeSheetByMonth()
        project_team_incident_time_sheet_by_month = ProjectTeamIncidentFixingTimeSheetByMonth()
        project_team_time_spent = ProjectTeamTimeSpent()
        quarter = Quarter(data_frame=input_data.quarters)
        quarter_time_sheet_by_date = QuarterTimeSheetByDate()
        quarter_time_sheet_by_date_model = QuarterTimeSheetByDateModel()
        skill = Skill(data_frame=input_data.skills)
        state_category = StateCategory(data_frame=input_data.state_categories)
        state = State(data_frame=input_data.states)
        system = System(data_frame=input_data.systems)
        system_change_request = SystemChangeRequest(data_frame=input_data.system_change_requests)
        system_change_request_analysis_time_sheet_by_date = SystemChangeRequestAnalysisTimeSheetByDate()
        system_change_request_developer = SystemChangeRequestDeveloper()
        system_change_request_development_time_sheet_by_date = SystemChangeRequestDevelopmentTimeSheetByDate()
        system_change_request_testing_time_sheet_by_date = SystemChangeRequestTestingTimeSheetByDate()
        system_change_request_time_sheet_by_date = SystemChangeRequestTimeSheetByDate()
        system_change_request_time_sheet_by_date_model = SystemChangeRequestTimeSheetByDateModel()
        system_change_request_time_spent = SystemChangeRequestTimeSpent()
        system_planning_period = SystemPlanningPeriod()
        system_planning_period_time_sheet_by_date = SystemPlanningPeriodTimeSheetByDate()
        system_planning_period_time_sheet_by_date_model = SystemPlanningPeriodTimeSheetByDateModel()
        system_planning_period_analysis_time_sheet_by_date = SystemPlanningPeriodAnalysisTimeSheetByDate()
        system_planning_period_analysis_time_sheet_by_date_model = SystemPlanningPeriodAnalysisTimeSheetByDateModel()
        system_planning_period_development_time_sheet_by_date = SystemPlanningPeriodDevelopmentTimeSheetByDate()
        system_planning_period_development_time_sheet_by_date_model = SystemPlanningPeriodDevelopmentTimeSheetByDateModel()
        system_planning_period_testing_time_sheet_by_date = SystemPlanningPeriodTestingTimeSheetByDate()
        system_planning_period_testing_time_sheet_by_date_model = SystemPlanningPeriodTestingTimeSheetByDateModel()
        system_time_spent = SystemTimeSpent()
        task = Task(data_frame=input_data.tasks)
        task_time_sheet = TaskTimeSheet(data_frame=input_data.task_time_sheets)
        task_time_sheet_by_date = TaskTimeSheetByDate()
        task_time_spent = TaskTimeSpent()
        work_item_time_sheet = WorkItemTimeSheet()
        work_items = WorkItem()

        data_source = cubista.DataSource(tables={
            change_request,
            change_request_analysis_time_sheet_by_date,
            change_request_calculated_date_after_quarter_end_issue,
            change_request_development_time_sheet_by_date,
            change_request_testing_time_sheet_by_date,
            change_request_time_sheet_by_date,
            change_request_time_sheet_by_date_model,
            change_request_time_spent,
            change_request_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter,
            companies,
            company_time_spent,
            company_time_sheet_by_date,
            company_time_sheet_by_date_model,
            dedicated_team,
            dedicated_team_dedicated_team_planning_period_position,
            dedicated_team_planning_period,
            dedicated_team_planning_period_position_person_time_spent,
            dedicated_team_planning_period_system,
            dedicated_team_planning_period_system_time_sheet_by_date,
            dedicated_team_planning_period_system_time_sheet_by_date_model,
            dedicated_team_planning_period_time_sheet_by_date,
            dedicated_team_planning_period_time_sheet_by_date_model,
            dedicated_team_planning_period_time_spent_previous_28_days,
            dedicated_team_quarter,
            dedicated_team_quarter_system,
            dedicated_team_quarter_system_time_sheet_by_date,
            dedicated_team_quarter_system_time_sheet_by_date_model,
            dedicated_team_quarter_time_sheet_by_date,
            dedicated_team_quarter_time_sheet_by_date_model,
            dedicated_team_position,
            dedicated_team_time_sheet_by_date,
            dedicated_team_time_sheet_by_date_model,
            dedicated_team_time_spent,
            epic,
            epic_analysis_time_sheet_by_date,
            epic_development_time_sheet_by_date,
            epic_system,
            epic_system_time_sheet_by_date,
            epic_system_time_sheet_by_date_model,
            epic_testing_time_sheet_by_date,
            epic_time_sheet_by_date,
            epic_time_sheet_by_date_model,
            function_component,
            function_component_kind,
            incident,
            incident_sub_task,
            incident_sub_task_time_sheet,
            incident_no_incident_sub_task_aggregation_time_sheet,
            incident_time_sheet,
            incident_time_sheet_by_date,
            incident_time_spent,
            non_project_activity,
            non_project_activity_time_sheets,
            project_team_position_person_plan_fact_issue,
            person,
            person_change_request_time_spent,
            person_dedicated_team_time_spent,
            person_dedicated_team_planning_period,
            person_epic,
            person_incident_month_time_spent,
            person_incident_time_spent,
            person_month,
            person_non_project_activity,
            person_non_project_activity_month,
            person_system_change_request,
            person_planning_period,
            person_project_team_month,
            person_project_team_persons_last_180_days_time_sheet,
            person_project_team_planning_period,
            person_project_team_time_spent,
            person_system_change_request,
            person_system_change_request_month_time_spent,
            person_system_change_request_time_sheet_by_date,
            person_system,
            person_task_month_time_spent,
            person_task_time_sheet_by_date,
            person_time_sheet_by_date,
            person_task_time_spent,
            persons_with_time_spent_for_change_requests_in_current_quarter_while_change_requests_not_in_current_quarter,
            planning_period,
            planning_period_time_sheet_by_date,
            planning_period_time_sheet_by_date_model,
            planning_period_time_spent,
            project_manager,
            project_manager_month,
            project_team,
            project_team_planning_period,
            project_team_planning_period_system,
            project_team_planning_period_system_time_sheet_by_date,
            project_team_planning_period_system_time_sheet_by_date_model,
            project_team_planning_period_time_sheet_by_date,
            project_team_planning_period_time_sheet_by_date_model,
            project_team_quarter,
            project_team_quarter_system,
            project_team_quarter_system_time_sheet_by_date,
            project_team_quarter_system_time_sheet_by_date_model,
            project_team_quarter_time_sheet_by_date,
            project_team_quarter_time_sheet_by_date_model,
            project_team_current_quarter,
            project_team_position,
            project_team_position_person_time_spent,
            project_team_position_person_time_spent_chronon,
            project_team_project_team_planning_period_position,
            project_team_time_sheet_by_date,
            project_team_time_sheet_by_date_model,
            project_team_time_sheet_by_month,
            project_team_analysis_time_sheet_by_month,
            project_team_development_time_sheet_by_month,
            project_team_testing_time_sheet_by_month,
            project_team_incident_time_sheet_by_month,
            project_team_time_spent,
            quarter,
            quarter_time_sheet_by_date,
            quarter_time_sheet_by_date_model,
            skill,
            state_category,
            state,
            system,
            system_change_request,
            system_change_request_analysis_time_sheet_by_date,
            system_change_request_developer,
            system_change_request_development_time_sheet_by_date,
            system_change_request_testing_time_sheet_by_date,
            management_time_sheet,
            system_change_request_time_sheet_by_date,
            system_change_request_time_sheet_by_date_model,
            system_change_request_time_spent,
            system_planning_period,
            system_planning_period_time_sheet_by_date,
            system_planning_period_time_sheet_by_date_model,
            system_planning_period_analysis_time_sheet_by_date,
            system_planning_period_analysis_time_sheet_by_date_model,
            system_planning_period_development_time_sheet_by_date,
            system_planning_period_development_time_sheet_by_date_model,
            system_planning_period_testing_time_sheet_by_date,
            system_planning_period_testing_time_sheet_by_date_model,
            system_time_spent,
            task,
            task_time_sheet,
            task_time_sheet_by_date,
            task_time_spent,
            work_item_time_sheet,
            work_items,
        })

        print("cubista done")

        output_data = OutputData()
        output_data.change_requests = data_source.tables[ChangeRequest].data_frame
        output_data.change_request_analysis_time_sheets_by_date = data_source.tables[ChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.change_request_calculated_date_after_quarter_end_issue = data_source.tables[ChangeRequestCalculatedDateAfterQuarterEndIssue].data_frame
        output_data.change_request_development_time_sheets_by_date = data_source.tables[ChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.change_request_testing_time_sheets_by_date = data_source.tables[ChangeRequestTestingTimeSheetByDate].data_frame
        output_data.change_request_time_sheets_by_date = data_source.tables[ChangeRequestTimeSheetByDate].data_frame
        output_data.change_request_time_sheet_by_date_model = data_source.tables[ChangeRequestTimeSheetByDateModel].data_frame
        output_data.change_request_time_spent = data_source.tables[ChangeRequestTimeSpent].data_frame
        output_data.change_request_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter = data_source.tables[ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter].data_frame
        output_data.companies = data_source.tables[Company].data_frame
        output_data.company_time_sheet_by_date = data_source.tables[CompanyTimeSheetByDate].data_frame
        output_data.company_time_sheet_by_date_model = data_source.tables[CompanyTimeSheetByDateModel].data_frame
        output_data.dedicated_team_dedicated_team_planning_period_positions = data_source.tables[DedicatedTeamDedicatedTeamPlanningPeriodPosition].data_frame
        output_data.dedicated_team_planning_periods = data_source.tables[DedicatedTeamPlanningPeriod].data_frame
        output_data.dedicated_team_planning_period_position_persons_time_spent = data_source.tables[DedicatedTeamPlanningPeriodPositionPersonTimeSpent].data_frame
        output_data.dedicated_team_planning_period_systems = data_source.tables[DedicatedTeamPlanningPeriodSystem].data_frame
        output_data.dedicated_team_planning_period_system_time_sheets_by_date = data_source.tables[DedicatedTeamPlanningPeriodSystemTimeSheetByDate].data_frame
        output_data.dedicated_team_planning_period_system_time_sheet_by_date_model = data_source.tables[DedicatedTeamPlanningPeriodSystemTimeSheetByDateModel].data_frame
        output_data.dedicated_team_planning_period_time_sheets_by_date = data_source.tables[DedicatedTeamPlanningPeriodTimeSheetByDate].data_frame
        output_data.dedicated_team_planning_period_time_sheets_by_date_model = data_source.tables[DedicatedTeamPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.dedicated_team_planning_period_time_spent_previous_28_days = data_source.tables[DedicatedTeamPlanningPeriodTimeSpentChronon].data_frame
        output_data.dedicated_team_quarter = data_source.tables[DedicatedTeamQuarter].data_frame
        output_data.dedicated_team_quarter_system = data_source.tables[DedicatedTeamQuarterSystem].data_frame
        output_data.dedicated_team_quarter_system_time_sheet_by_date = data_source.tables[DedicatedTeamQuarterSystemTimeSheetByDate].data_frame
        output_data.dedicated_team_quarter_system_time_sheet_by_date_model = data_source.tables[DedicatedTeamQuarterSystemTimeSheetByDateModel].data_frame
        output_data.dedicated_team_quarter_time_sheet_by_date = data_source.tables[DedicatedTeamQuarterTimeSheetByDate].data_frame
        output_data.dedicated_team_quarter_time_sheet_by_date_model = data_source.tables[DedicatedTeamQuarterSystemTimeSheetByDateModel].data_frame
        output_data.dedicated_team_positions = data_source.tables[DedicatedTeamPosition].data_frame
        output_data.dedicated_teams = data_source.tables[DedicatedTeam].data_frame
        output_data.dedicated_team_time_sheet_by_date = data_source.tables[DedicatedTeamTimeSheetByDate].data_frame
        output_data.dedicated_team_time_sheet_by_date_model = data_source.tables[DedicatedTeamTimeSheetByDateModel].data_frame
        output_data.dedicated_team_time_spent_previous_28_days = data_source.tables[DedicatedTeamTimeSpent].data_frame
        output_data.epics = data_source.tables[Epic].data_frame
        output_data.epic_analysis_time_sheets_by_date = data_source.tables[EpicAnalysisTimeSheetByDate].data_frame
        output_data.epic_development_time_sheets_by_date = data_source.tables[EpicDevelopmentTimeSheetByDate].data_frame
        output_data.epic_systems = data_source.tables[EpicSystem].data_frame
        output_data.epic_system_time_sheets_by_date = data_source.tables[EpicSystemTimeSheetByDate].data_frame
        output_data.epic_system_time_sheets_by_date_model = data_source.tables[EpicSystemTimeSheetByDateModel].data_frame
        output_data.epic_testing_time_sheets_by_date = data_source.tables[EpicTestingTimeSheetByDate].data_frame
        output_data.epic_time_sheets_by_date = data_source.tables[EpicTimeSheetByDate].data_frame
        output_data.epic_time_sheets_by_date_model = data_source.tables[EpicTimeSheetByDateModel].data_frame
        output_data.function_components = data_source.tables[FunctionComponent].data_frame
        output_data.function_component_kinds = data_source.tables[FunctionComponentKind].data_frame
        output_data.incidents = data_source.tables[Incident].data_frame
        output_data.incident_sub_task_time_sheet = data_source.tables[IncidentSubTaskTimeSheet].data_frame
        output_data.incident_sub_tasks = data_source.tables[IncidentSubTask].data_frame
        output_data.incident_time_sheet = data_source.tables[IncidentTimeSheet].data_frame
        output_data.incident_time_sheet_by_date = data_source.tables[IncidentTimeSheetByDate].data_frame
        output_data.non_project_activity = data_source.tables[NonProjectActivity].data_frame
        output_data.non_project_activity_time_sheets = data_source.tables[NonProjectActivityTimeSheet].data_frame
        output_data.project_team_position_person_plan_fact_issue = data_source.tables[ProjectTeamPositionPersonPlanFactIssue].data_frame
        output_data.persons = data_source.tables[Person].data_frame
        output_data.person_change_request_time_spent = data_source.tables[PersonChangeRequestTimeSpent].data_frame
        output_data.person_dedicated_team_time_spent = data_source.tables[PersonDedicatedTeamTimeSpent].data_frame
        output_data.person_dedicated_team_planning_period_time_spent = data_source.tables[PersonDedicatedTeamPlanningPeriod].data_frame
        output_data.person_epic_time_spent = data_source.tables[PersonEpic].data_frame
        output_data.person_incident_month_time_spent = data_source.tables[PersonIncidentMonthTimeSpent].data_frame
        output_data.person_incident_time_spent = data_source.tables[PersonIncidentTimeSpent].data_frame
        output_data.person_month = data_source.tables[PersonMonthTimeSpent].data_frame
        output_data.person_non_project_activity_time_spent = data_source.tables[PersonNonProjectActivityTimeSpent].data_frame
        output_data.person_non_project_activity_month_time_spent = data_source.tables[PersonNonProjectActivityMonthTimeSpent].data_frame
        output_data.person_planning_period_time_spent = data_source.tables[PersonPlanningPeriodTimeSpent].data_frame
        output_data.person_project_team_month = data_source.tables[PersonProjectTeamMonth].data_frame
        output_data.person_project_team_persons_last_180_days_time_sheet = data_source.tables[PersonProjectTeamPersonsLast180DaysTimeSheet].data_frame
        output_data.person_project_team_planning_period_time_spent = data_source.tables[PersonProjectTeamPlanningPeriodTimeSpent].data_frame
        output_data.person_project_team_time_spent = data_source.tables[PersonProjectTeamTimeSpent].data_frame
        output_data.person_system_change_request_month_time_spent = data_source.tables[PersonSystemChangeRequestMonthTimeSpent].data_frame
        output_data.person_system_change_request_time_sheet_by_date = data_source.tables[PersonSystemChangeRequestTimeSheetByDate].data_frame
        output_data.person_system_change_request_time_spent = data_source.tables[PersonSystemChangeRequestTimeSpent].data_frame
        output_data.person_system_time_spent = data_source.tables[PersonSystem].data_frame
        output_data.person_task_month_time_spent = data_source.tables[PersonTaskMonthTimeSpent].data_frame
        output_data.person_task_time_sheet_by_date = data_source.tables[PersonTaskTimeSheetByDate].data_frame
        output_data.person_task_time_spent = data_source.tables[PersonTaskTimeSpent].data_frame
        output_data.person_time_sheet_by_date = data_source.tables[PersonTimeSheetByDate].data_frame
        output_data.persons_with_time_spent_for_change_requests_in_current_quarter_while_change_requests_not_in_current_quarter = data_source.tables[PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter].data_frame
        output_data.planning_period_time_sheets_by_date = data_source.tables[PlanningPeriodTimeSheetByDate].data_frame
        output_data.planning_period_time_sheets_by_date_model = data_source.tables[PlanningPeriodTimeSheetByDateModel].data_frame
        output_data.planning_period_time_spent_previous_28_days = data_source.tables[PlanningPeriodTimeSpent].data_frame
        output_data.planning_periods = data_source.tables[PlanningPeriod].data_frame
        output_data.project_manager = data_source.tables[ProjectManager].data_frame
        output_data.project_manager_month = data_source.tables[ProjectManagerMonth].data_frame
        output_data.project_team_planning_period_time_sheets_by_date = data_source.tables[ProjectTeamPlanningPeriodTimeSheetByDate].data_frame
        output_data.project_team_planning_period_time_sheet_by_date_model = data_source.tables[ProjectTeamPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.project_team_planning_period_systems = data_source.tables[ProjectTeamPlanningPeriodSystem].data_frame
        output_data.project_team_planning_period_system_time_sheets_by_date = data_source.tables[ProjectTeamPlanningPeriodSystemTimeSheetByDate].data_frame
        output_data.project_team_planning_period_system_time_sheets_by_date_model = data_source.tables[ProjectTeamPlanningPeriodSystemTimeSheetByDateModel].data_frame
        output_data.project_team_planning_periods = data_source.tables[ProjectTeamPlanningPeriod].data_frame
        output_data.project_team_quarter = data_source.tables[ProjectTeamQuarter].data_frame
        output_data.project_team_quarter_system = data_source.tables[ProjectTeamQuarterSystem].data_frame
        output_data.project_team_quarter_system_time_sheet_by_date = data_source.tables[ProjectTeamQuarterSystemTimeSheetByDate].data_frame
        output_data.project_team_quarter_system_time_sheet_by_date_model = data_source.tables[ProjectTeamQuarterSystemTimeSheetByDateModel].data_frame
        output_data.project_team_quarter_time_sheet_by_date = data_source.tables[ProjectTeamQuarterTimeSheetByDate].data_frame
        output_data.project_team_quarter_time_sheet_by_date_model = data_source.tables[ProjectTeamQuarterTimeSheetByDateModel].data_frame
        output_data.project_team_quarter_time_spent_in_current_quarter = data_source.tables[ProjectTeamCurrentQuarter].data_frame
        output_data.project_team_positions = data_source.tables[ProjectTeamPosition].data_frame
        output_data.project_team_position_person_time_spent = data_source.tables[ProjectTeamPositionPersonTimeSpent].data_frame
        output_data.project_team_project_team_planning_period_positions = data_source.tables[ProjectTeamProjectTeamPlanningPeriodPosition].data_frame
        output_data.project_team_position_person_time_spent_chronon = data_source.tables[ProjectTeamPositionPersonTimeSpentChronon].data_frame
        output_data.project_teams = data_source.tables[ProjectTeam].data_frame
        output_data.project_team_time_sheet_by_date = data_source.tables[ProjectTeamTimeSheetByDate].data_frame
        output_data.project_team_time_sheet_by_date_model = data_source.tables[ProjectTeamTimeSheetByDateModel].data_frame
        output_data.project_team_time_sheet_by_month = data_source.tables[ProjectTeamTimeSheetByMonth].data_frame
        output_data.project_team_time_spent = data_source.tables[ProjectTeamTimeSpent].data_frame
        output_data.quarters = data_source.tables[Quarter].data_frame
        output_data.quarter_time_sheet_by_date = data_source.tables[QuarterTimeSheetByDate].data_frame
        output_data.skills = data_source.tables[Skill].data_frame
        output_data.states = data_source.tables[State].data_frame
        output_data.state_categories = data_source.tables[StateCategory].data_frame
        output_data.systems = data_source.tables[System].data_frame
        output_data.system_change_requests = data_source.tables[SystemChangeRequest].data_frame
        output_data.system_change_request_analysis_time_sheets_by_date = data_source.tables[SystemChangeRequestAnalysisTimeSheetByDate].data_frame
        output_data.system_change_request_developer = data_source.tables[SystemChangeRequestDeveloper].data_frame
        output_data.system_change_request_development_time_sheets_by_date = data_source.tables[SystemChangeRequestDevelopmentTimeSheetByDate].data_frame
        output_data.system_change_request_testing_time_sheets_by_date = data_source.tables[SystemChangeRequestTestingTimeSheetByDate].data_frame
        output_data.system_change_request_time_sheets = data_source.tables[ManagementTimeSheet].data_frame
        output_data.system_change_request_time_sheets_by_date = data_source.tables[SystemChangeRequestTimeSheetByDate].data_frame
        output_data.system_change_request_time_spent = data_source.tables[SystemChangeRequestTimeSpent].data_frame
        output_data.system_planning_periods = data_source.tables[SystemPlanningPeriod].data_frame
        output_data.system_planning_period_time_sheets_by_date = data_source.tables[SystemPlanningPeriodTimeSheetByDate].data_frame
        output_data.system_planning_period_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodTimeSheetByDateModel].data_frame
        output_data.system_planning_period_analysis_time_sheets_by_date = data_source.tables[SystemPlanningPeriodAnalysisTimeSheetByDate].data_frame
        output_data.system_planning_period_analysis_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodAnalysisTimeSheetByDateModel].data_frame
        output_data.system_planning_period_development_time_sheets_by_date = data_source.tables[SystemPlanningPeriodDevelopmentTimeSheetByDate].data_frame
        output_data.system_planning_period_development_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodDevelopmentTimeSheetByDateModel].data_frame
        output_data.system_planning_period_testing_time_sheets_by_date = data_source.tables[SystemPlanningPeriodTestingTimeSheetByDate].data_frame
        output_data.system_planning_period_testing_time_sheets_by_date_model = data_source.tables[SystemPlanningPeriodTestingTimeSheetByDateModel].data_frame
        output_data.system_time_spent = data_source.tables[SystemTimeSpent].data_frame
        output_data.task_time_sheets = data_source.tables[TaskTimeSheet].data_frame
        output_data.task_time_sheets_by_date = data_source.tables[TaskTimeSheetByDate].data_frame
        output_data.tasks = data_source.tables[Task].data_frame
        output_data.work_item_time_sheet = data_source.tables[WorkItemTimeSheet].data_frame
        output_data.work_items = data_source.tables[WorkItem].data_frame

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

        return output_data
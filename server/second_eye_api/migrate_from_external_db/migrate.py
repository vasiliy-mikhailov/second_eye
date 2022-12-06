from .transform import Transformer
import graphene_frame
from ..schema import change_request
from ..schema import company
from ..schema import dedicated_team
from ..schema import dedicated_team_planning_period
from ..schema import dedicated_team_quarter
from ..schema import epic
from ..schema import function_component
from ..schema import incident
from ..schema import incident_sub_task
from ..schema import issue
from ..schema import non_project_activity
from ..schema import person
from ..schema import person_change_request
from ..schema import person_dedicated_team
from ..schema import person_incident
from ..schema import person_incident_month
from ..schema import person_month
from ..schema import person_non_project_activity
from ..schema import person_non_project_activity_month
from ..schema import person_project_team
from ..schema import person_project_team_month
from ..schema import person_system
from ..schema import person_system_change_request
from ..schema import person_system_change_request_month
from ..schema import person_task
from ..schema import person_task_month
from ..schema import planning_period
from ..schema import project_manager
from ..schema import project_manager_month
from ..schema import project_team
from ..schema import project_team_planning_period
from ..schema import project_team_quarter
from ..schema import quarter
from ..schema import state
from ..schema import state_category
from ..schema import skill
from ..schema import system
from ..schema import system_change_request
from ..schema import task

def migrate(extractor):
    print("extract")
    input_data = extractor.extract()

    print("transform")
    transformer = Transformer(input_data=input_data)
    output_data = transformer.transform()

    print("done")
    return graphene_frame.DataStore(data_frames={
        change_request.ChangeRequest: output_data.change_requests,
        change_request.ChangeRequestTimeSheetsByDate: output_data.change_request_time_sheets_by_date,
        change_request.ChangeRequestAnalysisTimeSheetsByDate: output_data.change_request_analysis_time_sheets_by_date,
        change_request.ChangeRequestDevelopmentTimeSheetsByDate: output_data.change_request_development_time_sheets_by_date,
        change_request.ChangeRequestTestingTimeSheetsByDate: output_data.change_request_testing_time_sheets_by_date,
        company.Company: output_data.companies,
        company.CompanyTimeSheetsByDate: output_data.company_time_sheet_by_date,
        dedicated_team.DedicatedTeam: output_data.dedicated_teams,
        dedicated_team.DedicatedTeamPosition: output_data.dedicated_team_positions,
        dedicated_team.DedicatedTeamPositionAbility: output_data.dedicated_team_position_abilities,
        dedicated_team.DedicatedTeamTimeSheetsByDate: output_data.dedicated_team_time_sheet_by_date,
        dedicated_team_planning_period.DedicatedTeamPlanningPeriod: output_data.dedicated_team_planning_periods,
        dedicated_team_planning_period.DedicatedTeamPlanningPeriodPositionPersonTimeSpent: output_data.dedicated_team_planning_period_position_persons_time_spent,
        dedicated_team_planning_period.DedicatedTeamPlanningPeriodSystem: output_data.dedicated_team_planning_period_systems,
        dedicated_team_planning_period.DedicatedTeamPlanningPeriodSystemTimeSheetsByDate: output_data.dedicated_team_planning_period_system_time_sheets_by_date,
        dedicated_team_planning_period.DedicatedTeamPlanningPeriodTimeSheetsByDate: output_data.dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_quarter.DedicatedTeamQuarter: output_data.dedicated_team_quarter,
        dedicated_team_quarter.DedicatedTeamQuarterSystem: output_data.dedicated_team_quarter_system,
        dedicated_team_quarter.DedicatedTeamQuarterSystemTimeSheetsByDate: output_data.dedicated_team_quarter_system_time_sheet_by_date,
        dedicated_team_quarter.DedicatedTeamQuarterTimeSheetsByDate: output_data.dedicated_team_quarter_time_sheet_by_date,
        epic.Epic: output_data.epics,
        epic.EpicAnalysisTimeSheetsByDate: output_data.epic_analysis_time_sheets_by_date,
        epic.EpicDevelopmentTimeSheetsByDate: output_data.epic_development_time_sheets_by_date,
        epic.EpicSystem: output_data.epic_systems,
        epic.EpicSystemTimeSheetsByDate: output_data.epic_system_time_sheets_by_date,
        epic.EpicTestingTimeSheetsByDate: output_data.epic_testing_time_sheets_by_date,
        epic.EpicTimeSheetsByDate: output_data.epic_time_sheets_by_date,
        function_component.FunctionComponent: output_data.function_components,
        incident.Incident: output_data.incidents,
        incident_sub_task.IncidentSubTask: output_data.incident_sub_tasks,
        issue.ChangeRequestCalculatedDateAfterQuarterEndIssue: output_data.change_request_calculated_date_after_quarter_end_issue,
        issue.ProjectTeamPositionPersonPlanFactIssue: output_data.project_team_position_person_plan_fact_issue,
        non_project_activity.NonProjectActivity: output_data.non_project_activity,
        person.Person: output_data.persons,
        person.PersonEpicTimeSpent: output_data.person_epic_time_spent,
        person.PersonPlanningPeriodTimeSpent: output_data.person_planning_period_time_spent,
        person.PersonProjectTeamPlanningPeriodTimeSpent: output_data.person_project_team_planning_period_time_spent,
        person.PersonSystemChangeRequestTimeSheetsByDate: output_data.person_system_change_request_time_sheet_by_date,
        person_change_request.PersonChangeRequestTimeSpent: output_data.person_change_request_time_spent,
        person_dedicated_team.PersonDedicatedTeamTimeSpent: output_data.person_dedicated_team_time_spent,
        person_incident.PersonIncidentTimeSpent: output_data.person_incident_time_spent,
        person_incident_month.PersonIncidentMonthTimeSpent: output_data.person_incident_month_time_spent,
        person_month.PersonMonthTimeSpent: output_data.person_month,
        person_non_project_activity.PersonNonProjectActivityTimeSpent: output_data.person_non_project_activity_time_spent,
        person_non_project_activity_month.PersonNonProjectActivityMonthTimeSpent: output_data.person_non_project_activity_month_time_spent,
        person_project_team.PersonProjectTeamTimeSpent: output_data.person_project_team_time_spent,
        person_project_team_month.PersonProjectTeamMonth: output_data.person_project_team_month,
        person_system.PersonSystemTimeSpent: output_data.person_system_time_spent,
        person_system_change_request.PersonSystemChangeRequestTimeSpent: output_data.person_system_change_request_time_spent,
        person_system_change_request_month.PersonSystemChangeRequestMonthTimeSpent: output_data.person_system_change_request_month_time_spent,
        person_task.PersonTaskTimeSpent: output_data.person_task_time_spent,
        person_task_month.PersonTaskMonthTimeSpent: output_data.person_task_month_time_spent,
        planning_period.PlanningPeriod: output_data.planning_periods,
        planning_period.PlanningPeriodTimeSheetsByDate: output_data.planning_period_time_sheets_by_date,
        project_manager.ProjectManager: output_data.project_manager,
        project_manager_month.ProjectManagerMonth: output_data.project_manager_month,
        project_team.ProjectTeam: output_data.project_teams,
        project_team.ProjectTeamPosition: output_data.project_team_positions,
        project_team.ProjectTeamTimeSheetsByDate: output_data.project_team_time_sheet_by_date,
        project_team.ProjectTeamTimeSheetsByMonth: output_data.project_team_time_sheet_by_month,
        project_team.ProjectTeamPositionPersonTimeSpent: output_data.project_team_position_person_time_spent,
        project_team.ProjectTeamPositionPersonTimeSpentChronon: output_data.project_team_position_person_time_spent_chronon,
        project_team_planning_period.ProjectTeamPlanningPeriod: output_data.project_team_planning_periods,
        project_team_planning_period.ProjectTeamPlanningPeriodSystem: output_data.project_team_planning_period_systems,
        project_team_planning_period.ProjectTeamPlanningPeriodSystemTimeSheetsByDate: output_data.project_team_planning_period_system_time_sheets_by_date,
        project_team_planning_period.ProjectTeamPlanningPeriodTimeSheetsByDate: output_data.project_team_planning_period_time_sheets_by_date,
        project_team_planning_period.ProjectTeamPlanningPeriodPositionPersonTimeSpent: output_data.project_team_project_team_planning_period_position,
        project_team_quarter.ProjectTeamQuarter: output_data.project_team_quarter,
        project_team_quarter.ProjectTeamQuarterSystem: output_data.project_team_quarter_system,
        project_team_quarter.ProjectTeamQuarterSystemTimeSheetsByDate: output_data.project_team_quarter_system_time_sheet_by_date,
        project_team_quarter.ProjectTeamQuarterTimeSheetsByDate: output_data.project_team_quarter_time_sheet_by_date,
        quarter.ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter: output_data.change_request_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter,
        quarter.PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter: output_data.persons_with_time_spent_for_change_requests_in_current_quarter_while_change_requests_not_in_current_quarter,
        quarter.Quarter: output_data.quarters,
        quarter.QuarterTimeSheetsByDate: output_data.quarter_time_sheet_by_date,
        skill.Skill: output_data.skills,
        state.State: output_data.states,
        state_category.StateCategory: output_data.state_categories,
        system.System: output_data.systems,
        system_change_request.SystemChangeRequest: output_data.system_change_requests,
        system_change_request.SystemChangeRequestTimeSheetsByDate: output_data.system_change_request_time_sheets_by_date,
        system_change_request.SystemChangeRequestAnalysisTimeSheetsByDate: output_data.system_change_request_analysis_time_sheets_by_date,
        system_change_request.SystemChangeRequestDevelopmentTimeSheetsByDate: output_data.system_change_request_development_time_sheets_by_date,
        system_change_request.SystemChangeRequestTestingTimeSheetsByDate: output_data.system_change_request_testing_time_sheets_by_date,
        system.SystemPlanningPeriod: output_data.system_planning_periods,
        system.SystemPlanningPeriodTimeSheetsByDate: output_data.system_planning_period_time_sheets_by_date,
        system.SystemPlanningPeriodAnalysisTimeSheetsByDate: output_data.system_planning_period_analysis_time_sheets_by_date,
        system.SystemPlanningPeriodDevelopmentTimeSheetsByDate: output_data.system_planning_period_development_time_sheets_by_date,
        system.SystemPlanningPeriodTestingTimeSheetsByDate: output_data.system_planning_period_testing_time_sheets_by_date,
        task.Task: output_data.tasks,
    })
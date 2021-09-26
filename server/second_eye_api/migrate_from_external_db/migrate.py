import pandas as pd
from .transform import Transformer
import graphene_frame
from ..schema import change_request
from ..schema import company
from ..schema import dedicated_team
from ..schema import person
from ..schema import planning_period
from ..schema import project_team
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
        dedicated_team.DedicatedTeam: output_data.dedicated_teams,
        dedicated_team.DedicatedTeamPlanningPeriod: output_data.dedicated_team_planning_periods,
        dedicated_team.DedicatedTeamPlanningPeriodSystem: output_data.dedicated_team_planning_period_systems,
        dedicated_team.DedicatedTeamPlanningPeriodSystemTimeSheetsByDate: output_data.dedicated_team_planning_period_system_time_sheets_by_date,
        dedicated_team.DedicatedTeamPlanningPeriodTimeSheetsByDate: output_data.dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team.DedicatedTeamPosition: output_data.dedicated_team_positions,
        dedicated_team.DedicatedTeamPositionAbility: output_data.dedicated_team_position_abilities,
        person.Person: output_data.persons,
        planning_period.PlanningPeriod: output_data.planning_periods,
        planning_period.PlanningPeriodTimeSheetsByDate: output_data.planning_period_time_sheets_by_date,
        project_team.ProjectTeam: output_data.project_teams,
        project_team.ProjectTeamPlanningPeriod: output_data.project_team_planning_periods,
        project_team.ProjectTeamPlanningPeriodSystem: output_data.project_team_planning_period_systems,
        project_team.ProjectTeamPlanningPeriodSystemTimeSheetsByDate: output_data.project_team_planning_period_system_time_sheets_by_date,
        project_team.ProjectTeamPlanningPeriodTimeSheetsByDate: output_data.project_team_planning_period_time_sheets_by_date,
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
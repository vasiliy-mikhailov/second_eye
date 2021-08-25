import pandas as pd
from .extract import Extractor
from .transform import Transformer
import graphene_frame
from ..schema.change_request import \
    ChangeRequest, ChangeRequestTimeSheetsByDate, ChangeRequestAnalysisTimeSheetsByDate, \
    ChangeRequestDevelopmentTimeSheetsByDate, ChangeRequestTestingTimeSheetsByDate
from ..schema.company import Company
from ..schema.dedicated_team import \
    DedicatedTeam, DedicatedTeamPlanningPeriod, DedicatedTeamPlanningPeriodTimeSheetsByDate,\
    DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate, \
    DedicatedTeamPosition, DedicatedTeamPositionAbility
from ..schema.person import Person
from ..schema.planning_period import PlanningPeriod, PlanningPeriodTimeSheetsByDate, PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
from ..schema.project_team import \
    ProjectTeam, ProjectTeamPlanningPeriod, ProjectTeamPlanningPeriodTimeSheetsByDate, \
    ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
from ..schema.state import State
from ..schema.state_category import StateCategory
from ..schema.skill import Skill
from ..schema.system import System
from ..schema.system_change_request import \
    SystemChangeRequest, SystemChangeRequestTimeSheetsByDate, \
    SystemChangeRequestAnalysisTimeSheetsByDate, \
    SystemChangeRequestDevelopmentTimeSheetsByDate, SystemChangeRequestTestingTimeSheetsByDate

def migrate(get_input_connection):
    print("extract")
    extractor = Extractor(get_connection=get_input_connection)
    input_data = extractor.extract()

    print("transform")
    transformer = Transformer(input_data=input_data)
    output_data = transformer.transform()

    pd.set_option('display.min_rows', None)
    pd.set_option('display.max_columns', None)
    print(output_data.dedicated_team_positions)

    print("done")
    return graphene_frame.DataStore(data_frames={
        ChangeRequest: output_data.change_requests,
        ChangeRequestTimeSheetsByDate: output_data.change_request_time_sheets_by_date,
        ChangeRequestAnalysisTimeSheetsByDate: output_data.change_request_analysis_time_sheets_by_date,
        ChangeRequestDevelopmentTimeSheetsByDate: output_data.change_request_development_time_sheets_by_date,
        ChangeRequestTestingTimeSheetsByDate: output_data.change_request_testing_time_sheets_by_date,
        Company: output_data.companies,
        DedicatedTeam: output_data.dedicated_teams,
        DedicatedTeamPlanningPeriod: output_data.dedicated_team_planning_periods,
        DedicatedTeamPlanningPeriodTimeSheetsByDate: output_data.dedicated_team_planning_period_time_sheets_by_date,
        DedicatedTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate: output_data.dedicated_team_planning_period_time_spent_percent_with_value_and_without_value_by_date,
        DedicatedTeamPosition: output_data.dedicated_team_positions,
        DedicatedTeamPositionAbility: output_data.dedicated_team_position_abilities,
        Person: output_data.persons,
        PlanningPeriod: output_data.planning_periods,
        PlanningPeriodTimeSheetsByDate: output_data.planning_period_time_sheets_by_date,
        PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate: output_data.planning_period_time_spent_percent_with_value_and_without_value_by_date,
        ProjectTeam: output_data.project_teams,
        ProjectTeamPlanningPeriod: output_data.project_team_planning_periods,
        ProjectTeamPlanningPeriodTimeSheetsByDate: output_data.project_team_planning_period_time_sheets_by_date,
        ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate: output_data.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date,
        Skill: output_data.skills,
        State: output_data.states,
        StateCategory: output_data.state_categories,
        System: output_data.systems,
        SystemChangeRequest: output_data.system_change_requests,
        SystemChangeRequestTimeSheetsByDate: output_data.system_change_request_time_sheets_by_date,
        SystemChangeRequestAnalysisTimeSheetsByDate: output_data.system_change_request_analysis_time_sheets_by_date,
        SystemChangeRequestDevelopmentTimeSheetsByDate: output_data.system_change_request_development_time_sheets_by_date,
        SystemChangeRequestTestingTimeSheetsByDate: output_data.system_change_request_testing_time_sheets_by_date,
    })
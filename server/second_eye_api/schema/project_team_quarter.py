import graphene_frame

from . import change_request
from . import dedicated_team
from . import issue
from . import project_team
from . import project_team_quarter
from . import quarter
from . import system
from . import system_change_request

class ProjectTeamQuarter(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        quarter = graphene_frame.Field(to_entity=lambda: quarter.Quarter)
        quarter_key = graphene_frame.String()

        change_requests = graphene_frame.List(to_entity=lambda: change_request.ChangeRequest, to_field="project_team_quarter_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: project_team_quarter.ProjectTeamQuarterTimeSheetsByDate, to_field="project_team_quarter_id")

        project_team_quarter_systems = graphene_frame.List(
            to_entity=lambda: project_team_quarter.ProjectTeamQuarterSystem,
            to_field="project_team_quarter_id"
        )

        analysis_time_spent = graphene_frame.Float()
        development_time_spent = graphene_frame.Float()
        testing_time_spent = graphene_frame.Float()
        management_time_spent = graphene_frame.Float()
        incident_fixing_time_spent = graphene_frame.Float()
        time_spent = graphene_frame.Float()

        estimate = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        new_functions_time_spent_in_current_quarter = graphene_frame.Float()
        new_functions_time_spent_in_current_quarter_by_project_team = graphene_frame.Float()
        new_functions_time_spent_in_current_quarter_for_quarter_change_requests_share = graphene_frame.Float()

        resource_planning_error_numerator = graphene_frame.Float()
        resource_planning_error_denominator = graphene_frame.Float()
        resource_planning_error = graphene_frame.Float()

        change_request_calculated_date_after_quarter_end_issues = graphene_frame.List(
            to_entity=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            to_field="project_team_quarter_id"
        )

        change_request_calculated_date_after_quarter_end_issue_count = graphene_frame.Int()
        change_request_count = graphene_frame.Int()
        change_request_calculated_date_before_quarter_end_share = graphene_frame.Float()

class ProjectTeamQuarterTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        time_spent_with_value_percent_cumsum = graphene_frame.Float()
        time_spent_without_value_percent_cumsum = graphene_frame.Float()

        time_spent_for_reengineering_percent_cumsum = graphene_frame.Float()
        time_spent_not_for_reengineering_percent_cumsum = graphene_frame.Float()

        quarter = graphene_frame.Field(to_entity=lambda: ProjectTeamQuarter)

class ProjectTeamQuarterSystem(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        quarter = graphene_frame.Field(to_entity=lambda: quarter.Quarter)
        system = graphene_frame.Field(to_entity=lambda: system.System)

        system_change_requests = graphene_frame.List(to_entity=lambda: system_change_request.SystemChangeRequest, to_field="project_team_quarter_system_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: ProjectTeamQuarterSystemTimeSheetsByDate, to_field="project_team_quarter_system_id")

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

class ProjectTeamQuarterSystemTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

import graphene_frame

from . import change_request
from . import dedicated_team
from . import dedicated_team_quarter
from . import field_pack
from . import issue
from . import person
from . import planning_period
from . import project_team
from . import project_team_quarter
from . import quarter

class Quarter(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        name = graphene_frame.String()

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)

        start = graphene_frame.Date()
        end = graphene_frame.Date()

        project_teams = graphene_frame.ManyToMany(
            to_entity=lambda: project_team.ProjectTeam,
            to_field="project_team_id",
            through_entity=lambda: project_team_quarter.ProjectTeamQuarter,
            through_field="quarter_id"
        )

        dedicated_teams = graphene_frame.ManyToMany(
            to_entity=lambda: dedicated_team.DedicatedTeam,
            to_field="dedicated_team_id",
            through_entity=lambda: dedicated_team_quarter.DedicatedTeamQuarter,
            through_field="quarter_id"
        )

        dedicated_team_quarters = graphene_frame.List(
            to_entity=lambda: dedicated_team_quarter.DedicatedTeamQuarter,
            to_field="quarter_id"
        )

        project_team_quarters = graphene_frame.List(
            to_entity=lambda: project_team_quarter.ProjectTeamQuarter,
            to_field="quarter_id"
        )

        # systems = graphene_frame.ManyToMany(
        #     to_entity=lambda: system.System,
        #     to_field="system_id",
        #     through_entity=lambda: system.SystemQuarter,
        #     through_field="quarter_id"
        # )
        #
        # system_quarters = graphene_frame.List(
        #     to_entity=lambda: system.SystemQuarter,
        #     to_field="quarter_id"
        # )

        estimate = graphene_frame.Float()
        time_left = graphene_frame.Float()

        change_requests = graphene_frame.List(
            to_entity=lambda: change_request.ChangeRequest,
            to_field="quarter_id"
        )

        time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: QuarterTimeSheetsByDate,
            to_field="quarter_id"
        )

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        time_sheets_by_date_model_m = graphene_frame.Float()
        time_sheets_by_date_model_b = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        quarters = graphene_frame.List(to_entity=lambda: quarter.Quarter, to_field="quarter_id")

        change_request_calculated_date_after_quarter_end_issues = graphene_frame.List(
            to_entity=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            to_field="quarter_id"
        )

        change_request_calculated_date_after_quarter_end_issue_count = graphene_frame.Int()
        change_request_count = graphene_frame.Int()
        change_request_calculated_date_before_quarter_end_share = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]


class QuarterTimeSheetsByDate(graphene_frame.DataFrameObjectType):
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

        quarter = graphene_frame.Field(to_entity=lambda: Quarter)


class ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        change_request = graphene_frame.Field(to_entity=lambda: change_request.ChangeRequest)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        project_team_quarter = graphene_frame.Field(to_entity=lambda: project_team_quarter.ProjectTeamQuarter)
        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)
        dedicated_team_quarter = graphene_frame.Field(to_entity=lambda: dedicated_team_quarter.DedicatedTeamQuarter)
        quarter = graphene_frame.Field(to_entity=lambda: quarter.Quarter)
        time_spent_in_current_quarter = graphene_frame.Float()

class PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)
        project_team_quarter = graphene_frame.Field(to_entity=lambda: project_team_quarter.ProjectTeamQuarter)
        new_functions_time_spent_in_current_quarter = graphene_frame.Float()

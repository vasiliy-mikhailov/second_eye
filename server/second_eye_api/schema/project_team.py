import graphene_frame
from . import dedicated_team
from . import field_pack
from . import issue
from . import person
from . import project_team
from . import project_team_planning_period
from . import quarter
from . import state

class ProjectTeam(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        url = graphene_frame.String()
        name = graphene_frame.String()

        project_manager = graphene_frame.Field(to_entity=lambda: person.Person)

        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: ProjectTeamTimeSheetsByDate, to_field="project_team_id")

        time_sheets_by_month = graphene_frame.List(to_entity=lambda: ProjectTeamTimeSheetsByMonth, to_field="project_team_id")

        actual_change_request_capacity = graphene_frame.Float()
        estimate = graphene_frame.Float()
        time_left = graphene_frame.Float()
        queue_length = graphene_frame.Float()

        actual_analysis_capacity = graphene_frame.Float()
        analysis_time_left = graphene_frame.Float()
        analysis_queue_length = graphene_frame.Float()

        actual_development_capacity = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        development_queue_length = graphene_frame.Float()

        actual_testing_capacity = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        testing_queue_length = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

        new_functions_time_spent_in_current_quarter = graphene_frame.Float()

        project_team_planning_periods = graphene_frame.List(
            to_entity=lambda: project_team_planning_period.ProjectTeamPlanningPeriod,
            to_field="project_team_id"
        )

        positions = graphene_frame.List(
            to_entity=lambda: ProjectTeamPositionPersonTimeSpent,
            to_field="project_team_id"
        )

        chrononPositions = graphene_frame.List(
            to_entity=lambda: ProjectTeamPositionPersonTimeSpentChronon,
            to_field="project_team_id"
        )

        position_person_new_functions_plan_fact_issues = graphene_frame.List(
            to_entity=lambda: issue.ProjectTeamPositionPersonPlanFactIssue,
            to_field="project_team_id"
        )

        resource_planning_error_numerator = graphene_frame.Float()
        resource_planning_error_denominator = graphene_frame.Float()
        resource_planning_error = graphene_frame.Float()

        position_person_plan_fact_issue_count = graphene_frame.Int()

        time_spent_for_reengineering_percent = graphene_frame.Float()

        change_request_calculated_date_after_quarter_end_issues = graphene_frame.List(
            to_entity=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            to_field="project_team_id"
        )

        change_request_calculated_date_after_quarter_end_issue_count = graphene_frame.Int()

        change_requests_with_time_spent_in_current_quarter_while_it_is_not_in_current_quarter = graphene_frame.List(
            to_entity=lambda: quarter.ChangeRequestWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter,
            to_field="project_team_id"
        )

        persons_with_time_spent_for_change_requests_in_current_quarter_while_change_request_not_in_current_quarter = graphene_frame.List(
            to_entity=lambda: quarter.PersonsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter,
            to_field="project_team_id"
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class ProjectTeamTimeSheetsByDate(graphene_frame.DataFrameObjectType):
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
        project_team = graphene_frame.Field(to_entity=lambda: ProjectTeam)

class ProjectTeamTimeSheetsByMonth(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        month = graphene_frame.Date()

        analysis_time_spent_fte = graphene_frame.Float()
        development_time_spent_fte = graphene_frame.Float()
        testing_time_spent_fte = graphene_frame.Float()
        management_time_spent_fte = graphene_frame.Float()
        incident_fixing_time_spent_fte = graphene_frame.Float()
        non_project_activity_time_spent_fte = graphene_frame.Float()
        time_spent_fte = graphene_frame.Float()

        working_days_in_month_occured = graphene_frame.Float()
        project_team = graphene_frame.Field(to_entity=lambda: ProjectTeam)

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class ProjectTeamPositionPersonTimeSpent(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        position = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeamPosition)
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

        total_capacity = graphene_frame.Float()
        total_capacity_fte = graphene_frame.Float()

        resource_planning_error_numerator = graphene_frame.Float()
        resource_planning_error_denominator = graphene_frame.Float()
        resource_planning_error = graphene_frame.Float()
        plan_fact_fte_difference = graphene_frame.Float()
        state = graphene_frame.Field(to_entity=lambda: state.State)
    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class ProjectTeamPositionPersonTimeSpentChronon(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        position = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeamPosition)
        person = graphene_frame.Field(to_entity=lambda: person.Person)
        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

        total_capacity = graphene_frame.Float()
        total_capacity_fte = graphene_frame.Float()

        resource_planning_error_numerator = graphene_frame.Float()
        resource_planning_error_denominator = graphene_frame.Float()
        resource_planning_error = graphene_frame.Float()
        plan_fact_fte_difference = graphene_frame.Float()
        state = graphene_frame.Field(to_entity=lambda: state.State)
    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class ProjectTeamPosition(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()
        change_request_capacity = graphene_frame.Float()

        project_team = graphene_frame.Field(to_entity=lambda: ProjectTeam)

        person = graphene_frame.Field(to_entity=lambda: person.Person)

    def __str__(self):
        return self.name

import graphene_frame

from . import dedicated_team
from . import field_pack
from . import person_change_request
from . import planning_period
from . import project_team
from . import quarter
from . import state
from . import state_category
from . import system_change_request

class ChangeRequest(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        key = graphene_frame.String()
        url = graphene_frame.String()
        name = graphene_frame.String()

        analysis_express_estimate = graphene_frame.Float(nulls=True)
        development_express_estimate = graphene_frame.Float(nulls=True)
        testing_express_estimate = graphene_frame.Float(nulls=True)
        express_estimate = graphene_frame.Float(nulls=True)

        planned_install_date = graphene_frame.Date(nulls=True)

        planned_finish_date = graphene_frame.Date(nulls=True)

        calculated_finish_date = graphene_frame.Date()

        planned_install_date_delay_days = graphene_frame.Int(nulls=True)

        quarter_end_delay_days = graphene_frame.Int(nulls=True)

        planning_period_end_delay_days = graphene_frame.Int(nulls=True)

        delay_days = graphene_frame.Int(nulls=True)

        system_change_requests = graphene_frame.List(
            to_entity=lambda: system_change_request.SystemChangeRequest,
            to_field='change_request_id'
        )

        state = graphene_frame.Field(to_entity=lambda: state.State)

        has_value = graphene_frame.Boolean()
        is_reengineering = graphene_frame.Boolean()

        state_category_id = graphene_frame.Int()
        state_category = graphene_frame.Field(to_entity=lambda: state_category.StateCategory)

        dedicated_team = graphene_frame.Field(to_entity=lambda: dedicated_team.DedicatedTeam)

        project_team = graphene_frame.Field(to_entity=lambda: project_team.ProjectTeam)

        quarter = graphene_frame.Field(to_entity=lambda: quarter.Quarter)
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        #
        # dedicated_team_planning_period = models.ForeignKey(
        #     'DedicatedTeamPlanningPeriod', related_name='change_requests', on_delete=models.CASCADE
        # )
        #
        # project_team_planning_period = models.ForeignKey(
        #     'ProjectTeamPlanningPeriod', related_name='change_requests', on_delete=models.CASCADE
        # )
        #
        system_change_requests_analysis_estimate_sum = graphene_frame.Float()
        system_change_requests_development_estimate_sum = graphene_frame.Float()
        system_change_requests_testing_estimate_sum = graphene_frame.Float()
        system_change_requests_estimate_sum = graphene_frame.Float()

        analysis_estimate = graphene_frame.Float()
        development_estimate = graphene_frame.Float()
        testing_estimate = graphene_frame.Float()
        estimate = graphene_frame.Float()

        analysis_time_left = graphene_frame.Float()
        development_time_left = graphene_frame.Float()
        testing_time_left = graphene_frame.Float()
        time_left = graphene_frame.Float()

        actual_change_request_capacity = graphene_frame.Float()
        actual_analysis_capacity = graphene_frame.Float()
        actual_development_capacity = graphene_frame.Float()
        actual_testing_capacity = graphene_frame.Float()

        analysis_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: ChangeRequestAnalysisTimeSheetsByDate,
            to_field='change_request_id'
        )

        development_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: ChangeRequestDevelopmentTimeSheetsByDate,
            to_field='change_request_id'
        )

        testing_time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: ChangeRequestTestingTimeSheetsByDate,
            to_field='change_request_id'
        )

        time_sheets_by_date = graphene_frame.List(
            to_entity=lambda: ChangeRequestTimeSheetsByDate,
            to_field='change_request_id'
        )

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        persons = graphene_frame.List(to_entity=lambda: person_change_request.PersonChangeRequestTimeSpent, to_field="change_request_id")

        time_spent_in_current_quarter = graphene_frame.Float()

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPack(),
            lambda: field_pack.TimeSpentFieldPack(),
        ]

class ChangeRequestAnalysisTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        change_request = graphene_frame.Field(to_entity=lambda: ChangeRequest)

class ChangeRequestDevelopmentTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        change_request = graphene_frame.Field(to_entity=lambda: ChangeRequest)

class ChangeRequestTestingTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()

        change_request = graphene_frame.Field(to_entity=lambda: ChangeRequest)

class ChangeRequestTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        change_request = graphene_frame.Field(to_entity=lambda: ChangeRequest)

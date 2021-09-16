import graphene_frame
from . import planning_period
from . import system_change_request
from . import project_team

class System(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        name = graphene_frame.String()

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

class SystemPlanningPeriod(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: System)

        system_change_requests = graphene_frame.List(to_entity=lambda: system_change_request.SystemChangeRequest, to_field="system_planning_period_id")

        time_sheets_by_date = graphene_frame.List(to_entity=lambda: SystemPlanningPeriodTimeSheetsByDate, to_field="system_planning_period_id")
        time_spent_cumsum_at_end_prediction = graphene_frame.Float()

        analysis_time_sheets_by_date = graphene_frame.List(to_entity=lambda: SystemPlanningPeriodAnalysisTimeSheetsByDate, to_field="system_planning_period_id")
        analysis_time_spent_cumsum_at_end_prediction = graphene_frame.Float()

        development_time_sheets_by_date = graphene_frame.List(to_entity=lambda: SystemPlanningPeriodDevelopmentTimeSheetsByDate, to_field="system_planning_period_id")
        development_time_spent_cumsum_at_end_prediction = graphene_frame.Float()

        testing_time_sheets_by_date = graphene_frame.List(to_entity=lambda: SystemPlanningPeriodTestingTimeSheetsByDate, to_field="system_planning_period_id")
        testing_time_spent_cumsum_at_end_prediction = graphene_frame.Float()

        estimate = graphene_frame.Float()
        time_spent = graphene_frame.Float()
        time_left = graphene_frame.Float()

        analysis_estimate = graphene_frame.Float()
        development_estimate = graphene_frame.Float()
        testing_estimate = graphene_frame.Float()

        function_points = graphene_frame.Float()
        function_points_effort = graphene_frame.Float()
        effort_per_function_point = graphene_frame.Float()

        calculated_finish_date = graphene_frame.Date()

class SystemPlanningPeriodTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: System)

class SystemPlanningPeriodAnalysisTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: System)

class SystemPlanningPeriodDevelopmentTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: System)

class SystemPlanningPeriodTestingTimeSheetsByDate(graphene_frame.DataFrameObjectType):
    class Fields:
        id = graphene_frame.PrimaryKey(graphene_frame.Int())
        date = graphene_frame.Date()

        time_spent = graphene_frame.Float()
        time_spent_cumsum = graphene_frame.Float()
        time_spent_cumsum_prediction = graphene_frame.Float()

        planning_period = graphene_frame.Field(to_entity=lambda: planning_period.PlanningPeriod)
        system = graphene_frame.Field(to_entity=lambda: System)
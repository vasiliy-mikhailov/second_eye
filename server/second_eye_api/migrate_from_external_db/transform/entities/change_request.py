import cubista
from . import state
from . import project_team
import pandas as pd
from . import system_change_request
from . import dedicated_team
from . import task
from . import function_component

class ChangeRequest(cubista.Table):
    CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS = [
        "MKB-23539"
    ]

    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        express_estimate = cubista.FloatField(nulls=True)
        analysis_express_estimate = cubista.FloatField(nulls=True)
        development_express_estimate = cubista.FloatField(nulls=True)
        testing_express_estimate = cubista.FloatField(nulls=True)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default=-1, nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        planned_install_date = cubista.DateField(nulls=True)
        year_label_max = cubista.IntField(nulls=True)
        has_value = cubista.IntField()
        project_team_id = cubista.ForeignKeyField(foreign_table=lambda: project_team.ProjectTeam, default=-1, nulls=False)
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="company_id")

        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["install_date"].year if not pd.isnull(x["install_date"]) else (
                x["resolution_date"].year if not pd.isnull(x["resolution_date"]) else (
                    x["planned_install_date"].year if not pd.isnull(x["planned_install_date"]) else (
                        x["year_label_max"] if not pd.isnull(x["year_label_max"]) else -1
                    )
                )
            ),
            source_fields=["install_date", "resolution_date", "planned_install_date", "year_label_max"]
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        system_change_requests_analysis_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_development_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_testing_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        system_change_requests_estimate_sum = cubista.CalculatedField(
            lambda_expression=lambda x: x["system_change_requests_analysis_estimate_sum"] + x["system_change_requests_development_estimate_sum"] + x["system_change_requests_testing_estimate_sum"],
            source_fields=["system_change_requests_analysis_estimate_sum", "system_change_requests_development_estimate_sum", "system_change_requests_testing_estimate_sum"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="management_time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["analysis_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["analysis_express_estimate"] if not pd.isnull(x["analysis_express_estimate"]) else 0,
                        x["system_change_requests_analysis_estimate_sum"],
                        x["analysis_time_spent"]
                    )
                ),
            source_fields=["analysis_time_spent", "state_category_id", "analysis_express_estimate", "system_change_requests_analysis_estimate_sum"]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["development_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["development_express_estimate"] if not pd.isnull(x["development_express_estimate"]) else 0,
                        x["system_change_requests_development_estimate_sum"],
                        x["development_time_spent"]
                    )
                ),
            source_fields=["development_time_spent", "state_category_id", "development_express_estimate", "system_change_requests_development_estimate_sum"]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["testing_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["testing_express_estimate"] if not pd.isnull(x["testing_express_estimate"]) else 0,
                        x["system_change_requests_testing_estimate_sum"],
                        x["testing_time_spent"]
                    )
                ),
            source_fields=["testing_time_spent", "state_category_id", "testing_express_estimate", "system_change_requests_testing_estimate_sum"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate"]
        )

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        analysis_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["analysis_estimate"] - x["analysis_time_spent"],
            source_fields=["analysis_estimate", "analysis_time_spent"]
        )

        development_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["development_estimate"] - x["development_time_spent"],
            source_fields=["development_estimate", "development_time_spent"]
        )

        testing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["testing_estimate"] - x["testing_time_spent"],
            source_fields=["testing_estimate", "testing_time_spent"]
        )

        child_function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["id"] in ChangeRequest.CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS else x["child_function_points"],
            source_fields=["is_cancelled", "child_function_points", "id"]
        )

        child_function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            foreign_field_name="change_request_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or x["id"] in ChangeRequest.CHANGE_REQUESTS_WITHOUT_FUNCTION_POINTS else x["child_function_points_effort"],
            source_fields=["is_cancelled", "child_function_points_effort", "id"]
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

class ChangeRequestTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="planning_period_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )
        project_team_planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_planning_period_id"
        )

class ChangeRequestAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestAnalysisTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )

class ChangeRequestDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestDevelopmentTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )

class ChangeRequestTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTestingTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["change_request_id"], sort_by=["date"])
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="project_team_id"
        )
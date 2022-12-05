import cubista
import datetime

from . import change_request
from . import field_pack
from . import time_sheet

class PlanningPeriod(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.CalculatedField(lambda_expression=lambda x:
                str(x["id"]) if x["id"] != -1 else "Бэклог",
            source_fields=["id"]
        )

        start = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 1, 1) if x["id"] != -1 else datetime.date(datetime.date.today().year, 1, 1),
            source_fields=["id"]
        )

        end = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 12, 31) if x["id"] != -1 else datetime.date(datetime.date.today().year + 2, 12, 31),
            source_fields=["id"]
        )

        analysis_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        management_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"],
            source_fields=["management_time_spent"]
        )

        incident_fixing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"],
            source_fields=["incident_fixing_time_spent"]
        )

        non_project_activity_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent"],
            source_fields=["non_project_activity_time_spent"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"] + x["management_estimate"] + x["incident_fixing_estimate"] + x["non_project_activity_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate", "management_estimate", "incident_fixing_estimate", "non_project_activity_estimate"]
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

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                x["end"] if x["time_sheets_by_date_model_m"] < 1e-2 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )
            ),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.PlanningPeriodTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="planning_period_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="planning_period_id"
            ),
        ]

class PlanningPeriodTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: change_request.ChangeRequestTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]


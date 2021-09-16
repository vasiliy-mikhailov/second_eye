import cubista
import datetime
from . import change_request
from . import planning_period
from . import dedicated_team
from .. import planning_period_time_sheet_by_date_model
from ..utils import normalize

class PlanningPeriod(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.CalculatedField(lambda_expression=lambda x:
                str(x["id"]) if x["id"] != -1 else "Не указано",
            source_fields=["id"]
        )

        start = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 1, 1) if x["id"] != -1 else datetime.date(2100, 1, 1),
            source_fields=["id"]
        )

        end = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 12, 31) if x["id"] != -1 else datetime.date(2100, 1, 1),
            source_fields=["id"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="management_time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
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
            foreign_table=lambda: PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: PlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["start"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["end"] - x["start"]),
            source_fields=["start", "end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )


class PlanningPeriodTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: dedicated_team.DedicatedTeamPlanningPeriodTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["planning_period_id"], sort_by=["date"])

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: PlanningPeriodTimeSheetByDateModel,
            related_field_names=["planning_period_id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: PlanningPeriodTimeSheetByDateModel,
            related_field_names=["planning_period_id"],
            foreign_field_names=["planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )


class PlanningPeriodTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: PlanningPeriodTimeSheetByDate
        planning_period_id_field_name = "planning_period_id"

    class Fields:
        planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
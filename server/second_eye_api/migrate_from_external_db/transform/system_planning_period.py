import cubista
import datetime

from . import field_pack
from . import planning_period
from . import system_change_request
from . import time_sheet

class SystemPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        system_id = cubista.AggregatedTableGroupField(source="system_id", primary_key=False)
        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        time_left = cubista.AggregatedTableAggregateField(source="time_left", aggregate_function="sum")

        function_points = cubista.AggregatedTableAggregateField(source="function_points", aggregate_function="sum")
        function_points_effort = cubista.AggregatedTableAggregateField(source="function_points_effort", aggregate_function="sum")
        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        planning_period_start = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="start"
        )

        planning_period_end = planning_period.cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="end"
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                x["planning_period_end"] if x["time_sheets_by_date_model_m"] < 1e-2 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )
            ),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        analysis_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        analysis_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        analysis_time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        analysis_time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodAnalysisTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        analysis_calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["analysis_time_sheets_by_date_model_m"] == 0 else
                x["analysis_time_sheets_by_date_model_min_date"] + (x["analysis_estimate"] - x["analysis_time_sheets_by_date_model_b"]) / x["analysis_time_sheets_by_date_model_m"] * (x["analysis_time_sheets_by_date_model_max_date"] - x["analysis_time_sheets_by_date_model_min_date"]),
            source_fields=["analysis_time_sheets_by_date_model_min_date", "analysis_time_sheets_by_date_model_max_date", "planning_period_end", "analysis_estimate", "analysis_time_sheets_by_date_model_m", "analysis_time_sheets_by_date_model_b"]
        )

        development_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        development_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        development_time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        development_time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodDevelopmentTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        development_calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["development_time_sheets_by_date_model_m"] == 0 else
                x["development_time_sheets_by_date_model_min_date"] + (x["development_estimate"] - x["development_time_sheets_by_date_model_b"]) / x["development_time_sheets_by_date_model_m"] * (x["development_time_sheets_by_date_model_max_date"] - x["development_time_sheets_by_date_model_min_date"]),
            source_fields=["development_time_sheets_by_date_model_min_date", "development_time_sheets_by_date_model_max_date", "planning_period_end", "development_estimate", "development_time_sheets_by_date_model_m", "development_time_sheets_by_date_model_b"]
        )

        testing_time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        testing_time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        testing_time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        testing_time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTestingTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        testing_calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["testing_time_sheets_by_date_model_m"] == 0 else
                x["testing_time_sheets_by_date_model_min_date"] + (x["testing_estimate"] - x["testing_time_sheets_by_date_model_b"]) / x["testing_time_sheets_by_date_model_m"] * (x["testing_time_sheets_by_date_model_max_date"] - x["testing_time_sheets_by_date_model_min_date"]),
            source_fields=["testing_time_sheets_by_date_model_min_date", "testing_time_sheets_by_date_model_max_date", "planning_period_end", "testing_estimate", "testing_time_sheets_by_date_model_m", "testing_time_sheets_by_date_model_b"]
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.SystemPlanningPeriodTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["system_planning_period_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="system_planning_period_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="system_planning_period_id"
            ),
        ]
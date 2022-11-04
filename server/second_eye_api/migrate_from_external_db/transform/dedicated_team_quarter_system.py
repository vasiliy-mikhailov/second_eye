import datetime
import cubista

from . import dedicated_team_quarter
from . import field_pack
from . import project_team_quarter_system
from . import quarter
from . import time_sheet

class DedicatedTeamQuarterSystem(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team_quarter_system.ProjectTeamQuarterSystem
        sort_by: [str] = []
        group_by: [str] = ["quarter_id", "dedicated_team_id", "system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id", primary_key=False)
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id", primary_key=False)
        system_id = cubista.AggregatedTableGroupField(source="system_id", primary_key=False)

        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        management_time_spent = cubista.AggregatedTableAggregateField(source="management_time_spent", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_left = cubista.AggregatedTableAggregateField(source="time_left", aggregate_function="sum")

        function_points = cubista.AggregatedTableAggregateField(source="function_points", aggregate_function="sum")
        function_points_effort = cubista.AggregatedTableAggregateField(source="function_points_effort", aggregate_function="sum")
        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        quarter_start = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: quarter.Quarter,
            related_field_name="quarter_id",
            pulled_field_name="start"
        )

        quarter_end = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: quarter.Quarter,
            related_field_name="quarter_id",
            pulled_field_name="end"
        )

        dedicated_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_quarter.DedicatedTeamQuarter,
            related_field_names=["dedicated_team_id", "quarter_id"],
            foreign_field_names=["dedicated_team_id", "quarter_id"],
            pulled_field_name="id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_system_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                x["quarter_end"] if x["time_sheets_by_date_model_m"] == 0 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )
            ),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "quarter_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterSystemTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_system_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="dedicated_team_quarter_system_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="dedicated_team_quarter_system_id"
            ),
        ]
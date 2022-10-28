import datetime
import cubista
import pandas as pd

from . import change_request
from . import dedicated_team_quarter
from . import field_pack
from . import issue
from . import project_team
from . import project_team_quarter
from . import quarter
from . import state
from . import task
from . import time_sheet
from . import time_sheet_by_date_model
from . import utils

class DedicatedTeamQuarter(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team_quarter.ProjectTeamQuarter
        sort_by: [str] = []
        group_by: [str] = ["quarter_id", "dedicated_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id", primary_key=False)
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id", primary_key=False)

        quarter_key = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )

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

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["quarter_end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"]),
            source_fields=["time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "quarter_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        time_spent_for_reengineering_percent = cubista.PullMinByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamQuarterTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_quarter_id"],
            min_field_name="id",
            pulled_field_name="time_spent_for_reengineering_percent_cumsum",
            default=0
        )

        change_request_calculated_date_after_quarter_end_issue_count = cubista.AggregatedForeignField(
            foreign_table=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            foreign_field_name="dedicated_team_quarter_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        change_request_count = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="dedicated_team_quarter_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        change_request_calculated_date_before_quarter_end_share = cubista.CalculatedField(
            lambda_expression=lambda x: 1 - x["change_request_calculated_date_after_quarter_end_issue_count"] / x["change_request_count"] if x["change_request_count"] else 1,
            source_fields=["change_request_calculated_date_after_quarter_end_issue_count", "change_request_count"]
        )
    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]


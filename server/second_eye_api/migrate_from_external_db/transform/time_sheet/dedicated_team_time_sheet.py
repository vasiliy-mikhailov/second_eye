import cubista
import datetime

from .. import dedicated_team
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class DedicatedTeamTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ProjectTeamTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["dedicated_team_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["dedicated_team_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_with_value_cumsum = cubista.CumSumField(source_field="time_spent_with_value", group_by=["dedicated_team_id"], sort_by=["date"])
        time_spent_without_value_cumsum = cubista.CumSumField(source_field="time_spent_without_value", group_by=["dedicated_team_id"], sort_by=["date"])

        time_spent_with_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_with_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_with_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_without_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_without_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_without_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_for_reengineering", aggregate_function="sum")
        time_spent_not_for_reengineering = cubista.AggregatedTableAggregateField(source="time_spent_not_for_reengineering", aggregate_function="sum")
        time_spent_for_reengineering_cumsum = cubista.CumSumField(source_field="time_spent_for_reengineering", group_by=["dedicated_team_id"], sort_by=["date"])
        time_spent_not_for_reengineering_cumsum = cubista.CumSumField(source_field="time_spent_not_for_reengineering", group_by=["dedicated_team_id"], sort_by=["date"])

        time_spent_for_reengineering_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_for_reengineering_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_for_reengineering_cumsum", "time_spent_cumsum"]
        )

        time_spent_not_for_reengineering_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_not_for_reengineering_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_not_for_reengineering_cumsum", "time_spent_cumsum"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSheetByDateModel,
            related_field_names=["dedicated_team_id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSheetByDateModel,
            related_field_names=["dedicated_team_id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSheetByDateModel,
            related_field_names=["dedicated_team_id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSheetByDateModel,
            related_field_names=["dedicated_team_id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        company_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team.DedicatedTeam,
            related_field_names=["dedicated_team_id"],
            foreign_field_names=["id"],
            pulled_field_name="company_id",
            default=-1
        )

class DedicatedTeamTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: DedicatedTeamTimeSheetByDate
        entity_id_field_name = "dedicated_team_id"

    class Fields:
        dedicated_team_id = time_sheet_by_date_model.EntityIdField(source="dedicated_team_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")
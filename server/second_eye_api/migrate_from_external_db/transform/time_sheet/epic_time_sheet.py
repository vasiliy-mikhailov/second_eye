import cubista
import datetime

from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class EpicTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["epic_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["epic_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_with_value_cumsum = cubista.CumSumField(source_field="time_spent_with_value", group_by=["epic_id"], sort_by=["date"])
        time_spent_without_value_cumsum = cubista.CumSumField(source_field="time_spent_without_value", group_by=["epic_id"], sort_by=["date"])

        time_spent_with_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_with_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_with_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_without_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_without_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_without_value_cumsum", "time_spent_cumsum"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: EpicTimeSheetByDateModel,
            related_field_names=["epic_id"],
            foreign_field_names=["epic_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: EpicTimeSheetByDateModel,
            related_field_names=["epic_id"],
            foreign_field_names=["epic_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: EpicTimeSheetByDateModel,
            related_field_names=["epic_id"],
            foreign_field_names=["epic_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: EpicTimeSheetByDateModel,
            related_field_names=["epic_id"],
            foreign_field_names=["epic_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class EpicTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: EpicTimeSheetByDate
        entity_id_field_name = "epic_id"

    class Fields:
        epic_id = time_sheet_by_date_model.EntityIdField(source="epic_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")

class EpicAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestAnalysisTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["epic_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["epic_id"], sort_by=["date"])

class EpicDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestDevelopmentTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["epic_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["epic_id"], sort_by=["date"])

class EpicTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.ChangeRequestTestingTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["epic_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["epic_id"], sort_by=["date"])
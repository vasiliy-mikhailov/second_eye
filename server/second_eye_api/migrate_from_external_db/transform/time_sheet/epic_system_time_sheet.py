import cubista
import datetime

from .. import epic_system
from .. import time_sheet
from .. import time_sheet_by_date_model
from .. import utils

class EpicSystemTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["epic_id", "system_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")

        epic_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: epic_system.EpicSystem,
            related_field_names=["epic_id", "system_id"],
            foreign_field_names=["epic_id", "system_id"],
            pulled_field_name="id",
            default=-1
        )

        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["epic_id", "system_id"], sort_by=["date"])

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: EpicSystemTimeSheetByDateModel,
            related_field_names=["epic_system_id"],
            foreign_field_names=["epic_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: EpicSystemTimeSheetByDateModel,
            related_field_names=["epic_system_id"],
            foreign_field_names=["epic_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: EpicSystemTimeSheetByDateModel,
            related_field_names=["epic_system_id"],
            foreign_field_names=["epic_system_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: EpicSystemTimeSheetByDateModel,
            related_field_names=["epic_system_id"],
            foreign_field_names=["epic_system_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: utils.normalize(
                x=x["date"], min_x=x["time_sheets_by_date_model_min_date"],
                max_x=x["time_sheets_by_date_model_max_date"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )


class EpicSystemTimeSheetByDateModel(time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: time_sheet.EpicSystemTimeSheetByDate
        entity_id_field_name = "epic_system_id"

    class Fields:
        epic_system_id = time_sheet_by_date_model.EntityIdField(source="epic_system_id")
        time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
        time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
        time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")
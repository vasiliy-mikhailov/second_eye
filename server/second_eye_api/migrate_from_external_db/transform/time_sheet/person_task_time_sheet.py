import cubista
import datetime

from .. import field_pack
from .. import person
from .. import system_change_request
from .. import time_sheet

class PersonTaskTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = ["ordinal_date"]
        group_by: [str] = ["person_id", "task_id", "system_change_request_id", "change_request_id", "epic_id", "ordinal_date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        ordinal_date = cubista.AggregatedTableGroupField(source="ordinal_date")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")

        date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date.fromordinal(x["ordinal_date"]),
            source_fields=["ordinal_date"]
        )

        person_key = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )

        system_change_request_key = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
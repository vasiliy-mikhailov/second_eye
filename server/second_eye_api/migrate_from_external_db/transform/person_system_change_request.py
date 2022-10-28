import cubista

from . import field_pack
from . import person_planning_period
from . import system_change_request
from . import time_sheet
from . import work_item

class PersonSystemChangeRequestTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "system_change_request_id"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET, time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_TASK_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")

        system_change_request_key = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )

        system_change_request_name = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="name",
            default="Не указано"
        )

        effort_per_function_point = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="effort_per_function_point",
            default=0
        )


    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
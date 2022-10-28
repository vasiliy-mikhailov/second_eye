import cubista

from . import field_pack
from . import person_incident
from . import time_sheet

class PersonIncidentTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "incident_id"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_INCIDENT_NO_INCIDENT_SUB_TASK_AGGREGATION_TIME_SHEET, time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_INCIDENT_SUB_TASK_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        incident_id = cubista.AggregatedTableGroupField(source="incident_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
        ]

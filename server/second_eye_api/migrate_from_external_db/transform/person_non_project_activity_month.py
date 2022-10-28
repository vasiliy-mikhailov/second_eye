import cubista

from . import field_pack
from . import person_month
from . import person_non_project_activity
from . import time_sheet

class PersonNonProjectActivityMonthTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "non_project_activity_id", "month"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_NON_PROJECT_ACTIVITY_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        non_project_activity_id = cubista.AggregatedTableGroupField(source="non_project_activity_id")
        month = cubista.AggregatedTableGroupField(source="month")
        person_month_id = cubista.PullByRelatedField(
            foreign_table=lambda: person_month.PersonMonthTimeSpent,
            related_field_names=["person_id", "month"],
            foreign_field_names=["person_id", "month"],
            pulled_field_name="id",
            default=-1,
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPackForAggregatedTable(),
        ]

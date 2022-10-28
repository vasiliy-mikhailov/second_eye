import cubista

from . import field_pack
from . import person_month
from . import time_sheet

class PersonTaskMonthTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "task_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        task_id = cubista.AggregatedTableGroupField(source="task_id")
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
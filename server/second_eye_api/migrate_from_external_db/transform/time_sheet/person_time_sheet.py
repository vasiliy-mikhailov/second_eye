import cubista

from .. import time_sheet

class PersonTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["person_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["person_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
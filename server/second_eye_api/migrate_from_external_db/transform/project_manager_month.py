import cubista
import datetime

from . import field_pack
from . import time_sheet
from . import utils

class ProjectManagerMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = ["month"]
        group_by: [str] = ["project_manager_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_manager_id = cubista.AggregatedTableGroupField(source="project_manager_id")
        month = cubista.AggregatedTableGroupField(source="month")

        working_days_in_month_occured = cubista.CalculatedField(
            lambda_expression=lambda x: utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()),
            source_fields=["month"]
        )

        analysis_time_spent_fte = cubista.AggregatedTableAggregateField(source="analysis_time_spent_month_fte", aggregate_function="sum")
        development_time_spent_fte = cubista.AggregatedTableAggregateField(source="development_time_spent_month_fte", aggregate_function="sum")
        testing_time_spent_fte = cubista.AggregatedTableAggregateField(source="testing_time_spent_month_fte", aggregate_function="sum")
        management_time_spent_fte = cubista.AggregatedTableAggregateField(source="management_time_spent_month_fte", aggregate_function="sum")
        incident_fixing_time_spent_fte = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_month_fte", aggregate_function="sum")
        non_project_activity_time_spent_fte = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_month_fte", aggregate_function="sum")
        time_spent_fte = cubista.AggregatedTableAggregateField(source="time_spent_month_fte", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
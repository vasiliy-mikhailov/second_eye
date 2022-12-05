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
        group_by: [str] = ["person_id", "person_key", "system_change_request_id", "planning_period_id"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET, time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_TASK_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        person_key = cubista.AggregatedTableGroupField(source="person_key")
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        system_change_request_key = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")

        person_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: person_planning_period.PersonPlanningPeriodTimeSpent,
            related_field_names=["person_id", "planning_period_id"],
            foreign_field_names=["person_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

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

        system_change_request_effort_per_function_point = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="effort_per_function_point",
            default=0
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["management_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "management_time_spent"]
        )

        person_planning_period_function_points_effort = cubista.PullByRelatedField(
            foreign_table=lambda: person_planning_period.PersonPlanningPeriodTimeSpent,
            related_field_names=["person_id", "planning_period_id"],
            foreign_field_names=["person_id", "planning_period_id"],
            pulled_field_name="function_points_effort",
            default=0
        )

        percentage_of_person_total_time_in_planning_period = cubista.CalculatedField(
            lambda_expression=lambda x: x["function_points_effort"] / x["person_planning_period_function_points_effort"] if x["person_planning_period_function_points_effort"] else 1,
            source_fields=["function_points_effort", "person_planning_period_function_points_effort"]
        )

        effort_per_function_point_weighted_by_person_total_time_in_planning_period = cubista.CalculatedField(
            lambda_expression=lambda x: x["system_change_request_effort_per_function_point"] * x["percentage_of_person_total_time_in_planning_period"],
            source_fields=["system_change_request_effort_per_function_point", "percentage_of_person_total_time_in_planning_period"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
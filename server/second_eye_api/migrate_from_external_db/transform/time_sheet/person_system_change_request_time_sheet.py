import cubista

from .. import field_pack
from .. import person
from .. import person_system_change_request
from .. import system_change_request
from .. import time_sheet

class PersonSystemChangeRequestTimeSheetsByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["person_id", "system_change_request_id", "change_request_id", "epic_id", "date"]
        filter = lambda x: x["work_item_type"] in [time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_MANAGEMENT_TIME_SHEET, time_sheet.WorkItemTimeSheet.WORK_ITEM_TYPE_TASK_TIME_SHEET]
        filter_fields: [str] = ["work_item_type"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        person_key = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        system_change_request_key = cubista.PullByRelatedField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_names=["system_change_request_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default="-1"
        )
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")

        date = cubista.AggregatedTableGroupField(source="date")

        person_system_change_request_time_spent_id = cubista.PullByRelatedField(
            foreign_table=lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent,
            related_field_names=["person_id", "system_change_request_id"],
            foreign_field_names=["person_id", "system_change_request_id"],
            pulled_field_name="id",
            default=-1
        )

        person_planning_period_system_change_request_time_spent_id = cubista.PullByRelatedField(
            foreign_table=lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent,
            related_field_names=["person_id", "system_change_request_id"],
            foreign_field_names=["person_id", "system_change_request_id"],
            pulled_field_name="id",
            default=-1
        )

        system_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="system_id"
        )

        system_planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="system_planning_period_id"
        )

        project_team_planning_period_system_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="project_team_planning_period_system_id"
        )

        project_team_quarter_system_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="project_team_quarter_system_id"
        )

        function_points_effort = cubista.AggregatedTableAggregateField(source="function_points_effort", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
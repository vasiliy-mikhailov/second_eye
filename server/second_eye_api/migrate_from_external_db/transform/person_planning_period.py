import cubista
import datetime

from . import field_pack
from . import person
from . import person_planning_period
from . import person_system_change_request
from . import time_sheet
from . import utils

class PersonPlanningPeriodTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "planning_period_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")

        person_key = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="key",
            default=""
        )

        person_name = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_id"],
            foreign_field_names=["id"],
            pulled_field_name="name",
            default=""
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["management_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "management_time_spent"]
        )

        effort_per_function_point = cubista.AggregatedForeignField(
            foreign_table=lambda: person_system_change_request.PersonSystemChangeRequestTimeSpent,
            foreign_field_name="person_planning_period_id",
            aggregated_field_name="effort_per_function_point_weighted_by_person_total_time_in_planning_period",
            aggregate_function="sum",
            default=0
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

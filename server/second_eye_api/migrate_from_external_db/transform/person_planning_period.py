import cubista
import datetime

from . import field_pack
from . import person
from . import person_planning_period
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

        # effort_per_function_point = cubista.AggregatedTableAggregateField(source="effort_per_function_point", aggregate_function="sum")
        # time_spent_in_planning_period =

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

        # percentage_of_person_total_time_in_planning_period = cubista.CalculatedField(
        #     lambda_expression=lambda x: x["time_spent"] / x[
        #         "person_planning_period_time_spent"] if x[
        #         "person_planning_period_time_spent"] else 1,
        #     source_fields=["time_spent", "person_planning_period_time_spent"]
        # )
        #
        # effort_per_function_point_weighted_by_person_total_time_in_planning_period = cubista.CalculatedField(
        #     lambda_expression=lambda x: x["effort_per_function_point"] * x["percentage_of_person_total_time_in_planning_period"],
        #     source_fields=["effort_per_function_point", "percentage_of_person_total_time_in_planning_period"]
        # )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

import cubista
import datetime

from . import time_sheet
from . import utils

class PersonProjectTeamPlanningPeriodTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "project_team_planning_period_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        new_functions_time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")


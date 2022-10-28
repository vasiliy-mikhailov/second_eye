import cubista

from . import time_sheet
from . import utils

class ProjectTeamCurrentQuarter(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["project_team_quarter_id"]
        filter = lambda x: utils.is_in_current_quarter(for_date=x["date"])
        filter_fields: [str] = ["date"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        project_team_quarter_id = cubista.AggregatedTableGroupField(source="project_team_quarter_id")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
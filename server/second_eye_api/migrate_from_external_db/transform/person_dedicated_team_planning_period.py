import cubista

from . import field_pack
from . import person_dedicated_team_planning_period
from . import time_sheet

class PersonDedicatedTeamPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "dedicated_team_planning_period_id", "dedicated_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

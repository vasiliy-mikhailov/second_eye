import cubista

from . import field_pack
from . import time_sheet

class PersonProjectTeamMonth(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "person_key", "project_team_id", "month"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        person_key = cubista.AggregatedTableGroupField(source="person_key")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        month = cubista.AggregatedTableGroupField(source="month")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.MonthFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

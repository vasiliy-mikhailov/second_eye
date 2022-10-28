import cubista

from . import field_pack
from . import person
from . import time_sheet

class ProjectManager(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["project_manager_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableGroupField(source="project_manager_id", primary_key=True)
        key = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: person.Person, related_field_name="id", pulled_field_name="key")
        name = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: person.Person, related_field_name="id", pulled_field_name="name")
        is_active = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: person.Person, related_field_name="id", pulled_field_name="is_active")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]
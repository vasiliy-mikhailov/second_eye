import cubista
import datetime

from . import field_pack
from . import person_system
from . import time_sheet
from . import utils

class PersonSystem(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
        ]

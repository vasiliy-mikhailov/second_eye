import cubista
import datetime

from . import field_pack
from . import person
from . import time_sheet

class Person(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        name = cubista.StringField()
        is_active = cubista.IntField()
        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.PersonTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["person_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

        main_project_team_id = cubista.PullMaxByRelatedField(
            foreign_table=lambda: person.PersonProjectTeamPersonsLast180DaysTimeSheet,
            related_field_names=["id"],
            foreign_field_names=["person_id"],
            max_field_name="time_spent",
            pulled_field_name="project_team_id",
            default=-1
        )

        is_outsource = cubista.CalculatedField(
            lambda_expression=lambda x: x["key"].startswith("out_"),
            source_fields=["key"]
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="person_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: time_sheet.WorkItemTimeSheet,
                foreign_field_name="person_id"
            ),
        ]

class PersonProjectTeamPersonsLast180DaysTimeSheet(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["person_id", "project_team_id"]
        filter = lambda x: x["days_between_this_time_sheet_and_persons_last_time_sheet"] < 180
        filter_fields: [str] = ["days_between_this_time_sheet_and_persons_last_time_sheet"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")


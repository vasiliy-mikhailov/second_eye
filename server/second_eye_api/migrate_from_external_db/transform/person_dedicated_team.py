import cubista

from . import person_dedicated_team
from . import person_project_team
from . import time_sheet

class PersonDedicatedTeamTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: person_project_team.PersonProjectTeamTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["person_id", "dedicated_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")

        analysis_time_spent_chronon = cubista.AggregatedTableAggregateField(source="analysis_time_spent_chronon", aggregate_function="sum")
        development_time_spent_chronon = cubista.AggregatedTableAggregateField(source="development_time_spent_chronon", aggregate_function="sum")
        testing_time_spent_chronon = cubista.AggregatedTableAggregateField(source="testing_time_spent_chronon", aggregate_function="sum")
        management_time_spent_chronon = cubista.AggregatedTableAggregateField(source="management_time_spent_chronon", aggregate_function="sum")
        incident_fixing_time_spent_chronon = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_chronon", aggregate_function="sum")
        non_project_activity_time_spent_chronon = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_chronon", aggregate_function="sum")
        time_spent_chronon = cubista.AggregatedTableAggregateField(source="time_spent_chronon", aggregate_function="sum")

        analysis_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="analysis_time_spent_chronon_fte", aggregate_function="sum")
        development_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="development_time_spent_chronon_fte", aggregate_function="sum")
        testing_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="testing_time_spent_chronon_fte", aggregate_function="sum")
        management_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="management_time_spent_chronon_fte", aggregate_function="sum")
        incident_fixing_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_chronon_fte", aggregate_function="sum")
        non_project_activity_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_chronon_fte", aggregate_function="sum")
        time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="time_spent_chronon_fte", aggregate_function="sum")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

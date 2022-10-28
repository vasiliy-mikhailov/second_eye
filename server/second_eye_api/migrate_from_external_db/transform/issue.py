import cubista

from . import change_request
from . import dedicated_team_quarter
from . import project_team
from . import project_team_quarter
from . import state

class ProjectTeamPositionPersonPlanFactIssue(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team.ProjectTeamPositionPersonTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["position_id", "person_id", "project_team_id"]
        filter = lambda x: x["plan_fact_fte_difference"] > 0.4
        filter_fields: [str] = ["plan_fact_fte_difference"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        position_id = cubista.AggregatedTableGroupField(source="position_id", primary_key=False)
        person_id = cubista.AggregatedTableGroupField(source="person_id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        plan_fact_fte_difference = cubista.AggregatedTableAggregateField(source="plan_fact_fte_difference", aggregate_function="sum")

class ChangeRequestCalculatedDateAfterQuarterEndIssue(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: change_request.ChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["id", "project_team_id", "dedicated_team_id", "quarter_id"]
        filter = lambda x: x["quarter_id"] != -1 and x["state_category_id"] != state.StateCategory.DONE and x["quarter_end_delay_days"] > 0
        filter_fields: [str] = ["quarter_id", "state_category_id", "quarter_end_delay_days"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        change_request_id = cubista.AggregatedTableGroupField(source="id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id", primary_key=False)
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id", primary_key=False)
        quarter_end_delay_days = cubista.AggregatedTableAggregateField(source="quarter_end_delay_days", aggregate_function="sum")

        project_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_quarter.ProjectTeamQuarter,
            related_field_names=["project_team_id", "quarter_id"],
            foreign_field_names=["project_team_id", "quarter_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_quarter.DedicatedTeamQuarter,
            related_field_names=["dedicated_team_id", "quarter_id"],
            foreign_field_names=["dedicated_team_id", "quarter_id"],
            pulled_field_name="id",
            default=-1
        )


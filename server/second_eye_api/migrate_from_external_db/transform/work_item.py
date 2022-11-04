import cubista

from . import change_request
from . import field_pack
from . import incident
from . import non_project_activity
from . import project_team_planning_period
from . import time_sheet
from . import work_item

class WorkItem(cubista.UnionTable):
    class Union:
        tables: [cubista.Table] = [
            lambda: change_request.ChangeRequest,
            lambda: incident.Incident,
            lambda: non_project_activity.NonProjectActivity,
        ]

        fields: [str] = [
            "work_item_id",
            "planning_period_id",
            "project_team_id",
            "analysis_estimate",
            "development_estimate",
            "testing_estimate",
            "estimate",
            "analysis_time_spent",
            "development_time_spent",
            "testing_time_spent",
            "management_time_spent",
            "incident_fixing_time_spent",
            "non_project_activity_time_spent",
            "time_spent",
            "time_left",
            "function_points",
            "function_points_effort",
            "quarter_id",
        ]

    class Fields:
        id = cubista.UnionTableTableAutoIncrementPrimaryKeyField()
        work_item_id = cubista.UnionTableUnionField(source="work_item_id")
        planning_period_id = cubista.UnionTableUnionField(source="planning_period_id")
        project_team_id = cubista.UnionTableUnionField(source="project_team_id")
        analysis_estimate = cubista.UnionTableUnionField(source="analysis_estimate")
        development_estimate = cubista.UnionTableUnionField(source="development_estimate")
        testing_estimate = cubista.UnionTableUnionField(source="testing_estimate")
        estimate = cubista.UnionTableUnionField(source="estimate")
        analysis_time_spent = cubista.UnionTableUnionField(source="analysis_time_spent")
        development_time_spent = cubista.UnionTableUnionField(source="development_time_spent")
        testing_time_spent = cubista.UnionTableUnionField(source="testing_time_spent")
        management_time_spent = cubista.UnionTableUnionField(source="management_time_spent")
        incident_fixing_time_spent = cubista.UnionTableUnionField(source="incident_fixing_time_spent")
        non_project_activity_time_spent = cubista.UnionTableUnionField(source="non_project_activity_time_spent")
        time_spent = cubista.UnionTableUnionField(source="time_spent")
        time_left = cubista.UnionTableUnionField(source="time_left")
        function_points = cubista.UnionTableUnionField(source="function_points")
        function_points_effort = cubista.UnionTableUnionField(source="function_points_effort")
        quarter_id = cubista.UnionTableUnionField(source="quarter_id")

        time_spent_chronon = cubista.AggregatedForeignField(
            foreign_table=lambda: time_sheet.WorkItemTimeSheet,
            foreign_field_name="work_item_id",
            aggregated_field_name="time_spent_chronon",
            aggregate_function="sum",
            default=0
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )






import datetime
import cubista
import pandas as pd

from . import dedicated_team_planning_period
from . import field_pack
from . import incident_sub_task
from . import planning_period
from . import project_team
from . import project_team_planning_period
from . import quarter
from . import state
from . import system
from . import time_sheet
from . import utils

class Incident(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        system_id = cubista.ForeignKeyField(foreign_table=lambda: system.System, default=-1, nulls=False)
        project_team_id = cubista.ForeignKeyField(foreign_table=lambda: project_team.ProjectTeam, default=-1, nulls=False)
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="project_manager_id")
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        install_date = cubista.DateField(nulls=True)
        planned_install_date = cubista.DateField(nulls=True)
        year_label_max = cubista.IntField(nulls=True)
        work_item_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["id"],
            source_fields=["id"]
        )

        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: project_team.ProjectTeam, related_field_name="project_team_id", pulled_field_name="company_id")

        quarter_id = cubista.PullByRelatedField(
            foreign_table=lambda: quarter.Quarter,
            related_field_names=["quarter_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )

        quarter_key = cubista.CalculatedField(
            lambda_expression=lambda x: utils.get_quarter_key(x["install_date"]) if not pd.isnull(x["install_date"]) else (
                utils.get_quarter_key(x["resolution_date"]) if not pd.isnull(x["resolution_date"]) and x["state_category_id"] == state.StateCategory.DONE else (
                    utils.get_quarter_key(x["planned_install_date"]) if not pd.isnull(x["planned_install_date"]) else "-1"
                )
            ),
            source_fields=["install_date", "resolution_date", "state_category_id", "planned_install_date"]
        )

        planning_period_id = cubista.CalculatedField(
            lambda_expression=lambda x: x["install_date"].year if not pd.isnull(x["install_date"]) else (
                x["resolution_date"].year if not pd.isnull(x["resolution_date"]) and x["state_category_id"] == state.StateCategory.DONE else (
                    x["planned_install_date"].year if not pd.isnull(x["planned_install_date"]) else (
                        x["year_label_max"] if not pd.isnull(x["year_label_max"]) else -1
                    )
                )
            ),
            source_fields=["install_date", "resolution_date", "state_category_id", "planned_install_date", "year_label_max"]
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.date.today()
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.date.today()
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team_planning_period.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        management_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"],
            source_fields=["time_spent"]
        )

        analysis_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        development_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        testing_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        management_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        incident_sub_tasks_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: incident_sub_task.IncidentSubTask,
            foreign_field_name="incident_id",
            aggregated_field_name="time_spent",
            aggregate_function="sum",
            default=0
        )

        incident_no_sub_tasks_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: time_sheet.IncidentNoIncidentSubTaskAggregationTimeSheet,
            foreign_field_name="incident_id",
            aggregated_field_name="time_spent",
            aggregate_function="sum",
            default=0
        )

        incident_fixing_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_no_sub_tasks_time_spent"] + x["incident_sub_tasks_time_spent"],
            source_fields=["incident_no_sub_tasks_time_spent", "incident_sub_tasks_time_spent"]
        )

        non_project_activity_time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"],
            source_fields=["incident_fixing_time_spent"]
        )

        time_left = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        function_points_effort = cubista.CalculatedField(
            lambda_expression=lambda x: 0,
            source_fields=[]
        )

        time_spent_chronon = cubista.PullByRelatedField(
            foreign_table=lambda: IncidentTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["incident_id"],
            pulled_field_name="time_spent_chronon",
            default=0
        )

class IncidentTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.IncidentTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["incident_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        incident_id = cubista.AggregatedTableGroupField(source="incident_id")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
        ]
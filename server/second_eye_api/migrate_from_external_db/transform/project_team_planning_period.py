import cubista
import datetime

from . import dedicated_team_planning_period
from . import field_pack
from . import planning_period
from . import project_team
from . import project_team_planning_period
from . import time_sheet
from . import utils
from . import work_item

class ProjectTeamPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: work_item.WorkItem
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "project_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: project_team.ProjectTeam,
            related_field_name="project_team_id",
            pulled_field_name="dedicated_team_id"
        )
        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        time_left = cubista.AggregatedTableAggregateField(source="time_left", aggregate_function="sum")

        function_points = cubista.AggregatedTableAggregateField(source="function_points", aggregate_function="sum")
        function_points_effort = cubista.AggregatedTableAggregateField(source="function_points_effort", aggregate_function="sum")
        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        planning_period_start = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="start"
        )

        planning_period_end = planning_period.cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="end"
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )
            ),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamPlanningPeriodTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda:time_sheet.WorkItemTimeSheet,
                foreign_field_name="project_team_planning_period_id"
            ),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class ProjectTeamProjectTeamPlanningPeriodPosition(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: project_team.ProjectTeamPosition
        right_source_table: cubista.Table = lambda: project_team_planning_period.ProjectTeamPlanningPeriod
        left_fields = {
            "id": "position_id",
            "total_capacity": "total_capacity",
            "total_capacity_fte": "total_capacity_fte",
            "person_id": "person_id",
            "project_team_id": "project_team_id",
        }

        right_fields = {
            "project_team_id": "project_team_id",
            "id": "project_team_planning_period_id",
        }

        on_fields = ["project_team_id"]
    class Fields:
        id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
        position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
        person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
        project_team_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_id", default=-1)
        project_team_planning_period_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_planning_period_id", default=-1)
        total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
        total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)

class ProjectTeamPlanningPeriodPositionPersonTimeSpent(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: project_team_planning_period.ProjectTeamProjectTeamPlanningPeriodPosition
        right_source_table: cubista.Table = lambda: person_project_team_planning_period.PersonProjectTeamPlanningPeriod
        left_fields = {
            "position_id": "position_id",
            "total_capacity": "total_capacity",
            "total_capacity_fte": "total_capacity_fte",
            "person_id": "person_id",
            "project_team_id": "project_team_id",
            "project_team_planning_period_id": "project_team_planning_period_id",
        }

        right_fields = {
            "person_id": "person_id",
            "project_team_planning_period_id": "project_team_planning_period_id",
            "time_spent": "time_spent",
            "time_spent_chronon_fte": "time_spent_chronon_fte"
        }

        on_fields = ["person_id", "project_team_planning_period_id"]
    class Fields:
        id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
        position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
        person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
        project_team_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_id", default=-1)
        project_team_planning_period_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_planning_period_id", default=-1)
        total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
        total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)
        time_spent = cubista.OuterJoinedTableOuterJoinedField(source="time_spent", default=0)
        time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="time_spent_chronon_fte", default=0)

class ProjectTeamPlanningPeriodTimeSpentChronon(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["project_team_planning_period_id"]
        filter = lambda x: utils.is_in_chronon_bounds(for_date=x["date"], sys_date=datetime.date.today())
        filter_fields: [str] = ["date"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
import cubista
import datetime

from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import person_dedicated_team_planning_period
from . import planning_period
from . import project_team_planning_period
from . import time_sheet
from . import utils

class DedicatedTeamPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team_planning_period.ProjectTeamPlanningPeriod
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "dedicated_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id", primary_key=False)

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

        planning_period_end = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="end"
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"]),
            source_fields=["time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        time_spent_for_reengineering_percent = cubista.PullMinByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamPlanningPeriodTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_planning_period_id"],
            min_field_name="id",
            pulled_field_name="time_spent_for_reengineering_percent_cumsum",
            default=0
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class DedicatedTeamDedicatedTeamPlanningPeriodPosition(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: dedicated_team.DedicatedTeamPosition
        right_source_table: cubista.Table = lambda: dedicated_team_planning_period.DedicatedTeamPlanningPeriod
        left_fields = {
            "id": "position_id",
            "total_capacity": "total_capacity",
            "total_capacity_fte": "total_capacity_fte",
            "person_id": "person_id",
            "dedicated_team_id": "dedicated_team_id",
        }

        right_fields = {
            "dedicated_team_id": "dedicated_team_id",
            "id": "dedicated_team_planning_period_id",
        }

        on_fields = ["dedicated_team_id"]
    class Fields:
        id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
        position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
        person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
        dedicated_team_id = cubista.OuterJoinedTableOuterJoinedField(source="dedicated_team_id", default=-1)
        dedicated_team_planning_period_id = cubista.OuterJoinedTableOuterJoinedField(source="dedicated_team_planning_period_id", default=-1)
        total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
        total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)

class DedicatedTeamPlanningPeriodPositionPersonTimeSpent(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: dedicated_team_planning_period.DedicatedTeamDedicatedTeamPlanningPeriodPosition
        right_source_table: cubista.Table = lambda: person_dedicated_team_planning_period.PersonDedicatedTeamPlanningPeriod
        left_fields = {
            "position_id": "position_id",
            "total_capacity": "total_capacity",
            "total_capacity_fte": "total_capacity_fte",
            "person_id": "person_id",
            "dedicated_team_id": "dedicated_team_id",
            "dedicated_team_planning_period_id": "dedicated_team_planning_period_id",
        }

        right_fields = {
            "person_id": "person_id",
            "dedicated_team_planning_period_id": "dedicated_team_planning_period_id",
        }

        on_fields = ["person_id", "dedicated_team_planning_period_id"]
    class Fields:
        id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
        position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
        person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
        dedicated_team_id = cubista.OuterJoinedTableOuterJoinedField(source="dedicated_team_id", default=-1)
        dedicated_team_planning_period_id = cubista.OuterJoinedTableOuterJoinedField(source="dedicated_team_planning_period_id", default=-1)
        total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
        total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)

class DedicatedTeamPlanningPeriodTimeSpentPrevious28Days(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["dedicated_team_planning_period_id"]
        filter = lambda x: utils.is_in_chronon_bounds(for_date=x["date"], sys_date=datetime.date.today())
        filter_fields: [str] = ["date"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        new_functions_time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

# class ProjectTeamPositionPersonTimeSpent(cubista.OuterJoinedTable):
#     class OuterJoin:
#         left_source_table: cubista.Table = lambda: ProjectTeamPosition
#         right_source_table: cubista.Table = lambda: person_project_team.PersonProjectTeamTimeSpent
#         left_fields = {
#             "id": "position_id",
#             "total_capacity": "total_capacity",
#             "total_capacity_fte": "total_capacity_fte",
#             "person_id": "person_id",
#             "project_team_id": "project_team_id",
#             "state_id": "state_id",
#             "is_working": "is_working"
#         }
#
#         right_fields = {
#             "person_id": "person_id",
#             "project_team_id": "project_team_id",
#             "analysis_time_spent_chronon": "analysis_time_spent_chronon",
#             "development_time_spent_chronon": "development_time_spent_chronon",
#             "testing_time_spent_chronon": "testing_time_spent_chronon",
#             "management_time_spent_chronon": "management_time_spent_chronon",
#             "incident_fixing_time_spent_chronon": "incident_fixing_time_spent_chronon",
#             "non_project_activity_time_spent_chronon": "non_project_activity_time_spent_chronon",
#             "time_spent_chronon": "time_spent_chronon",
#
#             "analysis_time_spent_chronon_fte": "analysis_time_spent_chronon_fte",
#             "development_time_spent_chronon_fte": "development_time_spent_chronon_fte",
#             "testing_time_spent_chronon_fte": "testing_time_spent_chronon_fte",
#             "management_time_spent_chronon_fte": "management_time_spent_chronon_fte",
#             "incident_fixing_time_spent_chronon_fte": "incident_fixing_time_spent_chronon_fte",
#             "non_project_activity_time_spent_chronon_fte": "non_project_activity_time_spent_chronon_fte",
#             "time_spent_chronon_fte": "time_spent_chronon_fte",
#
#             "time_spent": "time_spent"
#         }
#
#         on_fields = ["person_id", "project_team_id"]
#     class Fields:
#         id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
#         position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
#         person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
#         project_team_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_id", default=-1)
#         state_id = cubista.OuterJoinedTableOuterJoinedField(source="state_id", default="-1")
#         is_working = cubista.OuterJoinedTableOuterJoinedField(source="is_working", default=True)
#
#         total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
#         total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)
#
#         analysis_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="analysis_time_spent_chronon", default=0)
#         development_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="development_time_spent_chronon", default=0)
#         testing_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="testing_time_spent_chronon", default=0)
#         management_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="management_time_spent_chronon", default=0)
#         incident_fixing_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="incident_fixing_time_spent_chronon", default=0)
#         non_project_activity_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="non_project_activity_time_spent_chronon", default=0)
#         time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="time_spent_chronon", default=0)
#
#         time_spent = cubista.OuterJoinedTableOuterJoinedField(source="time_spent", default=0)
#
#         analysis_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="analysis_time_spent_chronon_fte", default=0)
#         development_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="development_time_spent_chronon_fte", default=0)
#         testing_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="testing_time_spent_chronon_fte", default=0)
#         management_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="management_time_spent_chronon_fte", default=0)
#         incident_fixing_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="incident_fixing_time_spent_chronon_fte", default=0)
#         non_project_activity_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="non_project_activity_time_spent_chronon_fte", default=0)
#         time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="time_spent_chronon_fte", default=0)
#
#         plan_fact_fte_difference = cubista.CalculatedField(
#             lambda_expression=lambda x: abs(x["time_spent_chronon_fte"] - x["total_capacity_fte"]) if x["is_working"] else 0,
#             source_fields=["time_spent_chronon_fte", "total_capacity_fte", "is_working"]
#         )
#
#         resource_planning_error_numerator = cubista.CalculatedField(
#             lambda_expression=lambda x: x["plan_fact_fte_difference"] ** 2,
#             source_fields=["plan_fact_fte_difference"]
#         )
#
#         resource_planning_error_denominator = cubista.CalculatedField(
#             lambda_expression=lambda x: max(x["time_spent_chronon_fte"], x["total_capacity_fte"]) ** 2 if x["is_working"] else 0,
#             source_fields=["time_spent_chronon_fte", "total_capacity_fte", "is_working"]
#         )
#
#         resource_planning_error = cubista.CalculatedField(
#             lambda_expression=lambda x: math.sqrt(x["resource_planning_error_numerator"]) / math.sqrt(x["resource_planning_error_denominator"]) if x["resource_planning_error_denominator"] and x["is_working"] else 0,
#             source_fields=["resource_planning_error_numerator", "resource_planning_error_denominator", "is_working"]
#         )
#
# class ProjectTeamPositionPersonTimeSpentChronon(cubista.AggregatedTable):
#     class Aggregation:
#         source = lambda: project_team.ProjectTeamPositionPersonTimeSpent
#         sort_by: [str] = []
#         group_by: [str] = ["id", "position_id", "person_id", "project_team_id", "state_id", "is_working"]
#         filter = lambda x: x["total_capacity"] > 0 or x["time_spent_chronon"] > 0
#         filter_fields: [str] = ["total_capacity", "time_spent_chronon"]
#
#     class Fields:
#         id = cubista.AggregatedTableGroupField(source="id", primary_key=True)
#         position_id = cubista.AggregatedTableGroupField(source="position_id")
#         person_id = cubista.AggregatedTableGroupField(source="person_id")
#         project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
#         state_id = cubista.AggregatedTableGroupField(source="state_id")
#         is_working = cubista.AggregatedTableGroupField(source="is_working")
#
#         total_capacity = cubista.AggregatedTableAggregateField(source="total_capacity", aggregate_function="sum")
#         total_capacity_fte = cubista.AggregatedTableAggregateField(source="total_capacity_fte", aggregate_function="sum")
#         time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
#
#         plan_fact_fte_difference = cubista.AggregatedTableAggregateField(source="plan_fact_fte_difference", aggregate_function="sum")
#
#         resource_planning_error_numerator = cubista.AggregatedTableAggregateField(source="resource_planning_error_numerator", aggregate_function="sum")
#
#         resource_planning_error_denominator = cubista.AggregatedTableAggregateField(source="resource_planning_error_denominator", aggregate_function="sum")
#
#         resource_planning_error = cubista.AggregatedTableAggregateField(source="resource_planning_error", aggregate_function="sum")
#
#     class FieldPacks:
#         field_packs = [
#             lambda: field_pack.ChrononFieldPackForAggregatedTable(),
#         ]
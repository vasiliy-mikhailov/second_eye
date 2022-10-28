import cubista
import datetime
import math

from . import change_request
from . import dedicated_team
from . import field_pack
from . import incident
from . import issue
from . import person
from . import person_project_team
from . import person_project_team_planning_period
from . import project_team
from . import project_team_planning_period
from . import state
from . import time_sheet
from . import work_item

class ProjectTeam(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        project_manager_key = cubista.StringField()
        project_manager_id = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["project_manager_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )
        dedicated_team_id = cubista.ForeignKeyField(foreign_table=lambda: dedicated_team.DedicatedTeam, default=-1, nulls=False)
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: dedicated_team.DedicatedTeam, related_field_name="dedicated_team_id", pulled_field_name="company_id")

        analysis_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        management_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"],
            source_fields=["management_time_spent"]
        )

        incident_fixing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"],
            source_fields=["incident_fixing_time_spent"]
        )

        non_project_activity_estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent"],
            source_fields=["non_project_activity_time_spent"]
        )

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"] + x["management_estimate"] + x["incident_fixing_estimate"] + x["non_project_activity_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate", "management_estimate", "incident_fixing_estimate", "non_project_activity_estimate"]
        )

        analysis_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["analysis_estimate"] - x["analysis_time_spent"],
            source_fields=["analysis_estimate", "analysis_time_spent"]
        )

        development_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["development_estimate"] - x["development_time_spent"],
            source_fields=["development_estimate", "development_time_spent"]
        )

        testing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["testing_estimate"] - x["testing_time_spent"],
            source_fields=["testing_estimate", "testing_time_spent"]
        )

        management_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["management_estimate"] - x["management_time_spent"],
            source_fields=["management_estimate", "management_time_spent"]
        )

        incident_fixing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["incident_fixing_estimate"] - x["incident_fixing_time_spent"],
            source_fields=["incident_fixing_estimate", "incident_fixing_time_spent"]
        )

        non_project_activity_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["non_project_activity_estimate"] - x["non_project_activity_time_spent"],
            source_fields=["non_project_activity_estimate", "non_project_activity_time_spent"]
        )

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date(year=2100, month=12, day=31) if x["time_sheets_by_date_model_m"] == 0 else
                x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"]),
            source_fields=["time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        time_spent_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_spent_in_current_quarter",
            default=0
        )

        time_spent_not_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            pulled_field_name="time_spent_not_in_current_quarter",
            default=0
        )

        queue_length = cubista.CalculatedField(
            lambda_expression=lambda x: max((x["calculated_finish_date"] - datetime.date.today()).days / 30, 0) if x["time_left"] else 0,
            source_fields=["calculated_finish_date", "time_left"]
        )

        resource_planning_error_numerator = cubista.AggregatedForeignField(
            foreign_table=lambda: ProjectTeamPositionPersonTimeSpent,
            foreign_field_name="project_team_id",
            aggregated_field_name="resource_planning_error_numerator",
            aggregate_function="sum",
            default=0
        )

        resource_planning_error_denominator = cubista.AggregatedForeignField(
            foreign_table=lambda: ProjectTeamPositionPersonTimeSpent,
            foreign_field_name="project_team_id",
            aggregated_field_name="resource_planning_error_denominator",
            aggregate_function="sum",
            default=0
        )

        resource_planning_error = cubista.CalculatedField(
            lambda_expression=lambda x: math.sqrt(x["resource_planning_error_numerator"]) / math.sqrt(x["resource_planning_error_denominator"]) if x["resource_planning_error_denominator"] else 0,
            source_fields=["resource_planning_error_numerator", "resource_planning_error_denominator"]
        )

        position_person_plan_fact_issue_count = cubista.AggregatedForeignField(
            foreign_table=lambda: issue.ProjectTeamPositionPersonPlanFactIssue,
            foreign_field_name="project_team_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        change_request_calculated_date_after_quarter_end_issue_count = cubista.AggregatedForeignField(
            foreign_table=lambda: issue.ChangeRequestCalculatedDateAfterQuarterEndIssue,
            foreign_field_name="project_team_id",
            aggregated_field_name="id",
            aggregate_function="count",
            default=0
        )

        time_spent_for_reengineering_percent = cubista.PullMinByRelatedField(
            foreign_table=lambda: time_sheet.ProjectTeamTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["project_team_id"],
            min_field_name="id",
            pulled_field_name="time_spent_for_reengineering_percent_cumsum",
            default=0
        )
    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: project_team.ProjectTeamTimeSpent,
                foreign_field_name="project_team_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: project_team.ProjectTeamTimeSpent,
                foreign_field_name="project_team_id"
            ),
        ]

class ProjectTeamTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["project_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class ProjectTeamPosition(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        incident_capacity = cubista.FloatField()
        management_capacity = cubista.FloatField()
        change_request_capacity = cubista.FloatField()
        other_capacity = cubista.FloatField()
        total_capacity = cubista.CalculatedField(
            lambda_expression=lambda x: x["change_request_capacity"] + x["management_capacity"] + x["incident_capacity"] + x["other_capacity"],
            source_fields=["change_request_capacity", "management_capacity", "incident_capacity", "other_capacity"]
        )
        total_capacity_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["total_capacity"] / 8.0,
            source_fields=["total_capacity"]
        )
        person_key = cubista.StringField()
        person_id = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["person_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )
        project_team_id = cubista.ForeignKeyField(foreign_table=lambda: project_team.ProjectTeam, default=-1, nulls=False)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        state_name = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="name")
        is_working = cubista.CalculatedField(
            lambda_expression=lambda x: x["state_name"] == "Работает",
            source_fields=["state_name"]
        )

class ProjectTeamProjectTeamPlanningPeriodPosition(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: ProjectTeamPosition
        right_source_table: cubista.Table = lambda: project_team_planning_period.ProjectTeamPlanningPeriod
        left_fields = {
            "id": "position_id",
            "total_capacity": "total_capacity",
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

        total_capacity_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["total_capacity"] / 8.0,
            source_fields=["total_capacity"]
        )

class ProjectTeamPositionPersonTimeSpent(cubista.OuterJoinedTable):
    class OuterJoin:
        left_source_table: cubista.Table = lambda: ProjectTeamPosition
        right_source_table: cubista.Table = lambda: person_project_team.PersonProjectTeamTimeSpent
        left_fields = {
            "id": "position_id",
            "total_capacity": "total_capacity",
            "total_capacity_fte": "total_capacity_fte",
            "person_id": "person_id",
            "project_team_id": "project_team_id",
            "state_id": "state_id",
            "is_working": "is_working"
        }

        right_fields = {
            "person_id": "person_id",
            "project_team_id": "project_team_id",
            "analysis_time_spent_chronon": "analysis_time_spent_chronon",
            "development_time_spent_chronon": "development_time_spent_chronon",
            "testing_time_spent_chronon": "testing_time_spent_chronon",
            "management_time_spent_chronon": "management_time_spent_chronon",
            "incident_fixing_time_spent_chronon": "incident_fixing_time_spent_chronon",
            "non_project_activity_time_spent_chronon": "non_project_activity_time_spent_chronon",
            "time_spent_chronon": "time_spent_chronon",

            "analysis_time_spent_chronon_fte": "analysis_time_spent_chronon_fte",
            "development_time_spent_chronon_fte": "development_time_spent_chronon_fte",
            "testing_time_spent_chronon_fte": "testing_time_spent_chronon_fte",
            "management_time_spent_chronon_fte": "management_time_spent_chronon_fte",
            "incident_fixing_time_spent_chronon_fte": "incident_fixing_time_spent_chronon_fte",
            "non_project_activity_time_spent_chronon_fte": "non_project_activity_time_spent_chronon_fte",
            "time_spent_chronon_fte": "time_spent_chronon_fte",

            "time_spent": "time_spent"
        }

        on_fields = ["person_id", "project_team_id"]
    class Fields:
        id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
        position_id = cubista.OuterJoinedTableOuterJoinedField(source="position_id", default=-1)
        person_id = cubista.OuterJoinedTableOuterJoinedField(source="person_id", default=-1)
        project_team_id = cubista.OuterJoinedTableOuterJoinedField(source="project_team_id", default=-1)
        state_id = cubista.OuterJoinedTableOuterJoinedField(source="state_id", default="-1")
        is_working = cubista.OuterJoinedTableOuterJoinedField(source="is_working", default=True)

        total_capacity = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity", default=0)
        total_capacity_fte = cubista.OuterJoinedTableOuterJoinedField(source="total_capacity_fte", default=0)

        analysis_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="analysis_time_spent_chronon", default=0)
        development_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="development_time_spent_chronon", default=0)
        testing_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="testing_time_spent_chronon", default=0)
        management_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="management_time_spent_chronon", default=0)
        incident_fixing_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="incident_fixing_time_spent_chronon", default=0)
        non_project_activity_time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="non_project_activity_time_spent_chronon", default=0)
        time_spent_chronon = cubista.OuterJoinedTableOuterJoinedField(source="time_spent_chronon", default=0)

        time_spent = cubista.OuterJoinedTableOuterJoinedField(source="time_spent", default=0)

        analysis_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="analysis_time_spent_chronon_fte", default=0)
        development_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="development_time_spent_chronon_fte", default=0)
        testing_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="testing_time_spent_chronon_fte", default=0)
        management_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="management_time_spent_chronon_fte", default=0)
        incident_fixing_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="incident_fixing_time_spent_chronon_fte", default=0)
        non_project_activity_time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="non_project_activity_time_spent_chronon_fte", default=0)
        time_spent_chronon_fte = cubista.OuterJoinedTableOuterJoinedField(source="time_spent_chronon_fte", default=0)

        plan_fact_fte_difference = cubista.CalculatedField(
            lambda_expression=lambda x: abs(x["time_spent_chronon_fte"] - x["total_capacity_fte"]) if x["is_working"] else 0,
            source_fields=["time_spent_chronon_fte", "total_capacity_fte", "is_working"]
        )

        resource_planning_error_numerator = cubista.CalculatedField(
            lambda_expression=lambda x: x["plan_fact_fte_difference"] ** 2,
            source_fields=["plan_fact_fte_difference"]
        )

        resource_planning_error_denominator = cubista.CalculatedField(
            lambda_expression=lambda x: max(x["time_spent_chronon_fte"], x["total_capacity_fte"]) ** 2 if x["is_working"] else 0,
            source_fields=["time_spent_chronon_fte", "total_capacity_fte", "is_working"]
        )

        resource_planning_error = cubista.CalculatedField(
            lambda_expression=lambda x: math.sqrt(x["resource_planning_error_numerator"]) / math.sqrt(x["resource_planning_error_denominator"]) if x["resource_planning_error_denominator"] and x["is_working"] else 0,
            source_fields=["resource_planning_error_numerator", "resource_planning_error_denominator", "is_working"]
        )

class ProjectTeamPositionPersonTimeSpentChronon(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team.ProjectTeamPositionPersonTimeSpent
        sort_by: [str] = []
        group_by: [str] = ["id", "position_id", "person_id", "project_team_id", "state_id", "is_working"]
        filter = lambda x: x["total_capacity"] > 0 or x["time_spent_chronon"] > 0
        filter_fields: [str] = ["total_capacity", "time_spent_chronon"]

    class Fields:
        id = cubista.AggregatedTableGroupField(source="id", primary_key=True)
        position_id = cubista.AggregatedTableGroupField(source="position_id")
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        state_id = cubista.AggregatedTableGroupField(source="state_id")
        is_working = cubista.AggregatedTableGroupField(source="is_working")

        total_capacity = cubista.AggregatedTableAggregateField(source="total_capacity", aggregate_function="sum")
        total_capacity_fte = cubista.AggregatedTableAggregateField(source="total_capacity_fte", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

        plan_fact_fte_difference = cubista.AggregatedTableAggregateField(source="plan_fact_fte_difference", aggregate_function="sum")

        resource_planning_error_numerator = cubista.AggregatedTableAggregateField(source="resource_planning_error_numerator", aggregate_function="sum")

        resource_planning_error_denominator = cubista.AggregatedTableAggregateField(source="resource_planning_error_denominator", aggregate_function="sum")

        resource_planning_error = cubista.AggregatedTableAggregateField(source="resource_planning_error", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
        ]
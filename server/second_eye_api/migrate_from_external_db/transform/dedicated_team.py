import cubista
import datetime

from . import company
from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import person
from . import person_dedicated_team_planning_period
from . import project_team
from . import time_sheet
from . import utils

class DedicatedTeam(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        company_id = cubista.ForeignKeyField(foreign_table=lambda: company.Company, default=-1, nulls=False)
        cio_key = cubista.StringField()
        cio_id = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["cio_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )

        cto_key = cubista.StringField()
        cto_id = cubista.PullByRelatedField(
            foreign_table=lambda: person.Person,
            related_field_names=["cto_key"],
            foreign_field_names=["key"],
            pulled_field_name="id",
            default=-1
        )

        analysis_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
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

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_sheets_by_date_model_min_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_min_date",
            default=datetime.date.today()
        )

        time_sheets_by_date_model_max_date = cubista.PullByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_sheets_by_date_model_max_date",
            default=datetime.date.today()
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["last_timesheet_date"] if x["time_left"] == 0 else (
                datetime.date(year=2100, month=12, day=31) if x["time_sheets_by_date_model_m"] == 0 else (
                    x["time_sheets_by_date_model_min_date"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["time_sheets_by_date_model_max_date"] - x["time_sheets_by_date_model_min_date"])
                )
            ),
            source_fields=["last_timesheet_date", "time_left", "time_sheets_by_date_model_min_date", "time_sheets_by_date_model_max_date", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        time_spent_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_spent_in_current_quarter",
            default=0
        )

        time_spent_not_in_current_quarter = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamTimeSpent,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            pulled_field_name="time_spent_not_in_current_quarter",
            default=0
        )

        queue_length = cubista.CalculatedField(
            lambda_expression=lambda x: max((x["calculated_finish_date"] - datetime.date.today()).days / 30, 0) if x["time_left"] else 0,
            source_fields=["calculated_finish_date", "time_left"]
        )

        time_spent_for_reengineering_percent = cubista.PullMinByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            min_field_name="id",
            pulled_field_name="time_spent_for_reengineering_percent_cumsum",
            default=0
        )

        last_timesheet_date = cubista.PullMaxByRelatedField(
            foreign_table=lambda: time_sheet.DedicatedTeamTimeSheetByDate,
            related_field_names=["id"],
            foreign_field_names=["dedicated_team_id"],
            max_field_name="time_spent_cumsum",
            pulled_field_name="date",
            default=datetime.date.today()
        )

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: dedicated_team.DedicatedTeamTimeSpent,
                foreign_field_name="dedicated_team_id"
            ),
            lambda: field_pack.TimeSpentFieldPackAsAggregatedForeignFields(
                foreign_table=lambda: dedicated_team.DedicatedTeamTimeSpent,
                foreign_field_name="dedicated_team_id"
            ),
        ]

class DedicatedTeamTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.WorkItemTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["dedicated_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

class DedicatedTeamPosition(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        incident_capacity = cubista.FloatField()
        management_capacity = cubista.FloatField()
        change_request_capacity = cubista.FloatField()
        other_capacity = cubista.FloatField()
        person_id = cubista.ForeignKeyField(foreign_table=lambda: person.Person, default=-1, nulls=False)
        dedicated_team_id = cubista.ForeignKeyField(foreign_table=lambda: DedicatedTeam, default=-1, nulls=False)
        total_capacity = cubista.CalculatedField(
            lambda_expression=lambda x: x["change_request_capacity"] + x["management_capacity"] + x["incident_capacity"] + x["other_capacity"],
            source_fields=["change_request_capacity", "management_capacity", "incident_capacity", "other_capacity"]
        )
        total_capacity_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["total_capacity"] / 8.0,
            source_fields=["total_capacity"]
        )






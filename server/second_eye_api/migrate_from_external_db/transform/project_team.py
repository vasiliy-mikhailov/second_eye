import cubista
from . import project_team
from . import person
from . import dedicated_team
from . import change_request
from . import planning_period
from . import task
from . import function_component
import datetime
from . import system_change_request
from . import planning_period_time_sheet_by_date_model
from .utils import normalize

class ProjectTeam(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        dedicated_team_id = cubista.ForeignKeyField(foreign_table=lambda: dedicated_team.DedicatedTeam, default=-1, nulls=False)
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: dedicated_team.DedicatedTeam, related_field_name="dedicated_team_id", pulled_field_name="company_id")

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="project_team_id",
            aggregated_field_name="management_time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
        )

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

        estimate = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_estimate"] + x["development_estimate"] + x["testing_estimate"],
            source_fields=["analysis_estimate", "development_estimate", "testing_estimate"]
        )

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
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

class ProjectTeamPosition(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        incident_capacity = cubista.FloatField()
        management_capacity = cubista.FloatField()
        change_request_capacity = cubista.FloatField()
        other_capacity = cubista.FloatField()
        person_id = cubista.ForeignKeyField(foreign_table=lambda: person.Person, default="-1", nulls=False)
        project_team_id = cubista.ForeignKeyField(foreign_table=lambda: project_team.ProjectTeam, default=1, nulls=False)


class ProjectTeamPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: change_request.ChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "project_team_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ProjectTeam,
            related_field_name="project_team_id",
            pulled_field_name="dedicated_team_id"
        )
        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        management_time_spent = cubista.AggregatedTableAggregateField(source="management_time_spent", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
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
            foreign_table=lambda: dedicated_team.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["planning_period_start"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["planning_period_end"] - x["planning_period_start"]),
            source_fields=["planning_period_start", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class ProjectTeamPlanningPeriodTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: change_request.ChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["project_team_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_planning_period_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["project_team_planning_period_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        time_spent_with_value_cumsum = cubista.CumSumField(source_field="time_spent_with_value", group_by=["project_team_planning_period_id"], sort_by=["date"])
        time_spent_without_value_cumsum = cubista.CumSumField(source_field="time_spent_without_value", group_by=["project_team_planning_period_id"], sort_by=["date"])

        time_spent_with_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_with_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_with_value_cumsum", "time_spent_cumsum"]
        )

        time_spent_without_value_percent_cumsum = cubista.CalculatedField(
            lambda_expression=lambda x: 1 if x["time_spent_cumsum"] == 0 else x["time_spent_without_value_cumsum"] / x["time_spent_cumsum"],
            source_fields=["time_spent_without_value_cumsum", "time_spent_cumsum"]
        )

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_planning_period_id",
            default=-1
        )

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_id"],
            foreign_field_names=["project_team_planning_period_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )


class ProjectTeamPlanningPeriodTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ProjectTeamPlanningPeriodTimeSheetByDate
        planning_period_id_field_name = "project_team_planning_period_id"

    class Fields:
        project_team_planning_period_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="project_team_planning_period_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")

class ProjectTeamPlanningPeriodSystem(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequest
        sort_by: [str] = []
        group_by: [str] = ["planning_period_id", "project_team_id", "system_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id", primary_key=False)
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id", primary_key=False)
        system_id = cubista.AggregatedTableGroupField(source="system_id", primary_key=False)
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: ProjectTeam,
            related_field_name="project_team_id",
            pulled_field_name="dedicated_team_id"
        )
        analysis_estimate = cubista.AggregatedTableAggregateField(source="analysis_estimate", aggregate_function="sum")
        development_estimate = cubista.AggregatedTableAggregateField(source="development_estimate", aggregate_function="sum")
        testing_estimate = cubista.AggregatedTableAggregateField(source="testing_estimate", aggregate_function="sum")
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")

        management_time_spent = cubista.AggregatedTableAggregateField(source="management_time_spent", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
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
            foreign_table=lambda: dedicated_team.DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_id", "planning_period_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriod,
            related_field_names=["project_team_id", "planning_period_id"],
            foreign_field_names=["project_team_id", "planning_period_id"],
            pulled_field_name="id",
            default=-1
        )

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: dedicated_team.DedicatedTeamPlanningPeriodSystem,
            related_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
            foreign_field_names=["dedicated_team_id", "planning_period_id", "system_id"],
            pulled_field_name="id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_at_end_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: 1 * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

        calculated_finish_date = cubista.CalculatedField(
            lambda_expression=lambda x: x["planning_period_end"] if x["time_sheets_by_date_model_m"] == 0 else
                x["planning_period_start"] + (x["estimate"] - x["time_sheets_by_date_model_b"]) / x["time_sheets_by_date_model_m"] * (x["planning_period_end"] - x["planning_period_start"]),
            source_fields=["planning_period_start", "planning_period_end", "estimate", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class ProjectTeamPlanningPeriodSystemTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: system_change_request.SystemChangeRequestTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["project_team_planning_period_system_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        project_team_planning_period_system_id = cubista.AggregatedTableGroupField(source="project_team_planning_period_system_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["project_team_planning_period_system_id"], sort_by=["date"])

        dedicated_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_planning_period_id",
            default=-1
        )

        project_team_planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="project_team_planning_period_id",
            default=-1
        )

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="planning_period_id",
            default=-1
        )

        planning_period_start = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="start",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        planning_period_end = cubista.PullByRelatedField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_names=["planning_period_id"],
            foreign_field_names=["id"],
            pulled_field_name="end",
            default=datetime.datetime.date(datetime.datetime.now())
        )

        dedicated_team_planning_period_system_id = cubista.PullByRelatedField(
            foreign_table=lambda: project_team.ProjectTeamPlanningPeriodSystem,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["id"],
            pulled_field_name="dedicated_team_planning_period_system_id",
            default=-1
        )

        time_sheets_by_date_model_m = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_m",
            default=0
        )

        time_sheets_by_date_model_b = cubista.PullByRelatedField(
            foreign_table=lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDateModel,
            related_field_names=["project_team_planning_period_system_id"],
            foreign_field_names=["project_team_planning_period_system_id"],
            pulled_field_name="time_sheets_by_date_model_b",
            default=0
        )

        time_spent_cumsum_prediction = cubista.CalculatedField(
            lambda_expression=lambda x: normalize(
                x=x["date"], min_x=x["planning_period_start"],
                max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
            source_fields=["date", "planning_period_start", "planning_period_end", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )

class ProjectTeamPlanningPeriodSystemTimeSheetByDateModel(planning_period_time_sheet_by_date_model.ModelTable):
    class Model:
        source = lambda: ProjectTeamPlanningPeriodSystemTimeSheetByDate
        planning_period_id_field_name = "project_team_planning_period_system_id"

    class Fields:
        project_team_planning_period_system_id = planning_period_time_sheet_by_date_model.PeriodIdField(source="project_team_planning_period_system_id")
        time_sheets_by_date_model_m = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = planning_period_time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
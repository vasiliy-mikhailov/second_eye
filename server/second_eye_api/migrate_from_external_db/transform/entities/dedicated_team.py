import cubista
from . import company
from . import person
from . import project_team
from . import planning_period
from . import function_component
from . import change_request
import datetime

class DedicatedTeam(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        company_id = cubista.ForeignKeyField(foreign_table=lambda: company.Company, default=-1, nulls=False)

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: project_team.ProjectTeam,
            foreign_field_name="dedicated_team_id",
            aggregated_field_name="management_time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
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

class DedicatedTeamPosition(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        incident_capacity = cubista.FloatField()
        management_capacity = cubista.FloatField()
        change_request_capacity = cubista.FloatField()
        other_capacity = cubista.FloatField()
        person_id = cubista.ForeignKeyField(foreign_table=lambda: person.Person, default="-1", nulls=False)
        dedicated_team_id = cubista.ForeignKeyField(foreign_table=lambda: DedicatedTeam, default=1, nulls=False)

class DedicatedTeamPlanningPeriod(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team.ProjectTeamPlanningPeriod
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

        planning_period_end = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: planning_period.PlanningPeriod,
            related_field_name="planning_period_id",
            pulled_field_name="end"
        )

class DedicatedTeamPlanningperiodTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: project_team.ProjectTeamPlanningperiodTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["dedicated_team_planning_period_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

        dedicated_team_planning_period_id = cubista.AggregatedTableGroupField(source="dedicated_team_planning_period_id")
        date = cubista.AggregatedTableGroupField(source="date")

        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["dedicated_team_planning_period_id"], sort_by=["date"])

        planning_period_id = cubista.PullByRelatedField(
            foreign_table=lambda: DedicatedTeamPlanningPeriod,
            related_field_names=["dedicated_team_planning_period_id"],
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

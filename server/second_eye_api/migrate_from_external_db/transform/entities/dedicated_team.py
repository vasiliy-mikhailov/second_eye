import cubista
from . import company
from . import person
from . import project_team
from . import planning_period

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
        estimate = cubista.AggregatedTableAggregateField(source="estimate", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_left = cubista.AggregatedTableAggregateField(source="time_left", aggregate_function="sum")
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
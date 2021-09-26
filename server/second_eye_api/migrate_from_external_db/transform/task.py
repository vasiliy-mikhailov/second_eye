import cubista
from . import skill
from . import system_change_request
from . import state
from . import person
import pandas as pd
from . import dedicated_team
from . import project_team
from . import function_component
from . import system

class Task(cubista.Table):
    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        skill_id = cubista.ForeignKeyField(foreign_table=lambda: skill.Skill, default=-1, nulls=False)
        preliminary_estimate = cubista.FloatField(nulls=True)
        planned_estimate = cubista.FloatField(nulls=True)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default=-1, nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        system_change_request_id = cubista.ForeignKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            default="-1",
            nulls=False
        )

        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="change_request_id")
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="project_team_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="company_id")

        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="has_value")

        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="system_id")
        system_has_function_points = cubista.PullByForeignPrimaryKeyField(lambda: system.System, related_field_name="system_id", pulled_field_name="has_function_points")

        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="planning_period_id"
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

        time_spent = cubista.AggregatedForeignField(foreign_table=lambda: TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="time_spent", aggregate_function="sum", default=0)

        estimate = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                max(
                    x["planned_estimate"] if not pd.isnull(x["planned_estimate"]) else (
                        x["preliminary_estimate"] if not pd.isnull(
                            x["preliminary_estimate"]) else 0
                    ),
                    x["time_spent"]
                )
            ),
            source_fields=["time_spent", "state_category_id", "planned_estimate", "preliminary_estimate"]
        )

        time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] - x["time_spent"],
            source_fields=["estimate", "time_spent"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="analysis_time_spent", aggregate_function="sum", default=0)
        analysis_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            (
                x["time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["planned_estimate"] if not pd.isnull(x["planned_estimate"]) else (
                            x["preliminary_estimate"] if not pd.isnull(
                                x["preliminary_estimate"]) else 0
                        ),
                        x["time_spent"]
                    )
                )
            ) if x["skill_id"] == skill.Skill.ANALYSIS else 0,
            source_fields=["time_spent", "skill_id", "state_category_id", "planned_estimate", "preliminary_estimate"]
        )
        analysis_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["analysis_estimate"] - x["analysis_time_spent"],
            source_fields=["analysis_estimate", "analysis_time_spent"]
        )

        development_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="development_time_spent", aggregate_function="sum", default=0)
        development_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            (
                x["time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["planned_estimate"] if not pd.isnull(x["planned_estimate"]) else (
                            x["preliminary_estimate"] if not pd.isnull(
                                x["preliminary_estimate"]) else 0
                        ),
                        x["time_spent"]
                    )
                )
            ) if x["skill_id"] == skill.Skill.DEVELOPMENT else 0,
            source_fields=["time_spent", "skill_id", "state_category_id", "planned_estimate", "preliminary_estimate"]
        )
        development_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["development_estimate"] - x["development_time_spent"],
            source_fields=["development_estimate", "development_time_spent"]
        )

        testing_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="testing_time_spent", aggregate_function="sum", default=0)
        testing_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            (
                x["time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["planned_estimate"] if not pd.isnull(x["planned_estimate"]) else (
                            x["preliminary_estimate"] if not pd.isnull(
                                x["preliminary_estimate"]) else 0
                        ),
                        x["time_spent"]
                    )
                )
            ) if x["skill_id"] == skill.Skill.TESTING else 0,
            source_fields=["time_spent", "skill_id", "state_category_id", "planned_estimate", "preliminary_estimate"]
        )
        testing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["testing_estimate"] - x["testing_time_spent"],
            source_fields=["testing_estimate", "testing_time_spent"]
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

        child_function_points = cubista.AggregatedForeignField(
            foreign_table=lambda: function_component.FunctionComponent,
            foreign_field_name="task_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or not x["system_has_function_points"] else x["child_function_points"],
            source_fields=["is_cancelled", "child_function_points", "system_has_function_points"]
        )

class TaskTimeSheet(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        task_id = cubista.ForeignKeyField(foreign_table=lambda: Task, default="-1", nulls=False)
        date = cubista.DateField(nulls=False)
        time_spent = cubista.FloatField(nulls=False)
        person_id = cubista.ForeignKeyField(foreign_table=lambda: person.Person, default="-1", nulls=False)

        task_id = cubista.ForeignKeyField(foreign_table=lambda: Task, default="-1", nulls=False)
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="system_change_request_id")
        change_request_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="change_request_id")
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="project_team_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="company_id")
        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="has_value")
        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="system_id")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="planning_period_id")
        skill_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: Task, related_field_name="task_id", pulled_field_name="skill_id")

        analysis_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.ANALYSIS else 0,
            source_fields=["time_spent", "skill_id"]
        )

        development_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.DEVELOPMENT else 0,
            source_fields=["time_spent", "skill_id"]
        )

        testing_time_spent = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["skill_id"] == skill.Skill.TESTING else 0,
            source_fields=["time_spent", "skill_id"]
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

        time_spent_with_value = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["has_value"] else 0,
            source_fields=["time_spent", "has_value"]
        )

        time_spent_without_value = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if not x["has_value"] else 0,
           source_fields=["time_spent", "has_value"]
        )

class TaskTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: TaskTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["task_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["date"])
        time_spent_with_value = cubista.AggregatedTableAggregateField(source="time_spent_with_value", aggregate_function="sum")
        time_spent_without_value = cubista.AggregatedTableAggregateField(source="time_spent_without_value", aggregate_function="sum")
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: Task,
            related_field_name="task_id",
            pulled_field_name="system_change_request_id"
        )

class TaskAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: TaskTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["task_id", "date"]
        filter = lambda x: x["skill_id"] == skill.Skill.ANALYSIS
        filter_fields: [str] = ["skill_id"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["date"])
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: Task,
            related_field_name="task_id",
            pulled_field_name="system_change_request_id"
        )

class TaskDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: TaskTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["task_id", "date"]
        filter = lambda x: x["skill_id"] == skill.Skill.DEVELOPMENT
        filter_fields: [str] = ["skill_id"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["date"])
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: Task,
            related_field_name="task_id",
            pulled_field_name="system_change_request_id"
        )

class TaskTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: TaskTimeSheet
        sort_by: [str] = ["date"]
        group_by: [str] = ["task_id", "date"]
        filter = lambda x: x["skill_id"] == skill.Skill.TESTING
        filter_fields: [str] = ["skill_id"]

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["date"])
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: Task,
            related_field_name="task_id",
            pulled_field_name="system_change_request_id"
        )
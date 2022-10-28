import cubista

from . import dedicated_team
from . import dedicated_team_planning_period
from . import field_pack
from . import function_component
from . import project_team
from . import project_team_planning_period
from . import skill
from . import state
from . import system
from . import system_change_request
from . import time_sheet

class Task(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        skill_id = cubista.ForeignKeyField(foreign_table=lambda: skill.Skill, default=-1, nulls=False)
        time_left = cubista.FloatField(nulls=False)
        time_original_estimate = cubista.FloatField(nulls=False)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        system_change_request_id = cubista.ForeignKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            default=-1,
            nulls=False
        )

        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="change_request_id")
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="project_team_id")
        project_manager_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="project_manager_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="dedicated_team_id")

        epic_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="epic_id"
        )

        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="company_id")

        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="has_value")
        is_reengineering = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="is_reengineering")

        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="system_id")
        system_has_function_points = cubista.PullByForeignPrimaryKeyField(lambda: system.System, related_field_name="system_id", pulled_field_name="has_function_points")

        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="planning_period_id"
        )

        quarter_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: system_change_request.SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="quarter_id"
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

        time_spent = cubista.AggregatedForeignField(foreign_table=lambda: time_sheet.TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="time_spent", aggregate_function="sum", default=0)

        estimate = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                x["time_spent"] + x["time_left"]
            ),
            source_fields=["time_spent", "state_category_id", "time_left"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: time_sheet.TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="analysis_time_spent", aggregate_function="sum", default=0)
        analysis_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] if x["skill_id"] == skill.Skill.ANALYSIS else 0,
            source_fields=["estimate", "skill_id"]
        )
        analysis_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_left"] if x["skill_id"] == skill.Skill.ANALYSIS else 0,
            source_fields=["time_left", "skill_id"]
        )

        development_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: time_sheet.TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="development_time_spent", aggregate_function="sum", default=0)
        development_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] if x["skill_id"] == skill.Skill.DEVELOPMENT else 0,
            source_fields=["estimate", "skill_id"]
        )
        development_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_left"] if x["skill_id"] == skill.Skill.DEVELOPMENT else 0,
            source_fields=["time_left", "skill_id"]
        )

        testing_time_spent = cubista.AggregatedForeignField(foreign_table=lambda: time_sheet.TaskTimeSheet, foreign_field_name="task_id", aggregated_field_name="testing_time_spent", aggregate_function="sum", default=0)
        testing_estimate = cubista.CalculatedField(lambda_expression=lambda x:
            x["estimate"] if x["skill_id"] == skill.Skill.TESTING else 0,
            source_fields=["estimate", "skill_id"]
        )
        testing_time_left = cubista.CalculatedField(lambda_expression=lambda x:
            x["time_left"] if x["skill_id"] == skill.Skill.TESTING else 0,
            source_fields=["time_left", "skill_id"]
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

class TaskTimeSpent(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: time_sheet.TaskTimeSheet
        sort_by: [str] = []
        group_by: [str] = ["task_id", "system_change_request_id", "change_request_id", "project_team_id", "dedicated_team_id", "company_id", "planning_period_id", "quarter_id", "system_id", "epic_id", "person_id"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        task_id = cubista.AggregatedTableGroupField(source="task_id")
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        change_request_id = cubista.AggregatedTableGroupField(source="change_request_id")
        project_team_id = cubista.AggregatedTableGroupField(source="project_team_id")
        dedicated_team_id = cubista.AggregatedTableGroupField(source="dedicated_team_id")
        company_id = cubista.AggregatedTableGroupField(source="company_id")
        planning_period_id = cubista.AggregatedTableGroupField(source="planning_period_id")
        quarter_id = cubista.AggregatedTableGroupField(source="quarter_id")
        system_id = cubista.AggregatedTableGroupField(source="system_id")
        epic_id = cubista.AggregatedTableGroupField(source="epic_id")
        person_id = cubista.AggregatedTableGroupField(source="person_id")
        new_functions_time_spent_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_in_current_quarter", aggregate_function="sum")
        new_functions_time_spent_not_in_current_quarter = cubista.AggregatedTableAggregateField(source="time_spent_not_in_current_quarter", aggregate_function="sum")

    class FieldPacks:
        field_packs = [
            lambda: field_pack.ChrononFieldPackForAggregatedTable(),
            lambda: field_pack.TimeSpentFieldPackForAggregatedTable(),
        ]

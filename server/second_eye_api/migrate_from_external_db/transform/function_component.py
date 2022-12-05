import cubista
from . import state
from . import task
from . import change_request
from . import dedicated_team_planning_period
from . import project_team_planning_period
from . import system_change_request
from . import system

class FunctionComponent(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        key = cubista.StringField(primary_key=False, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default="-1", nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        is_cancelled = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="is_cancelled")
        task_id = cubista.ForeignKeyField(foreign_table=lambda: task.Task, default=-1, nulls=False)
        system_change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: task.Task,
            related_field_name="task_id", pulled_field_name="system_change_request_id"
        )
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: task.Task,
            related_field_name="task_id", pulled_field_name="change_request_id"
        )
        project_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: task.Task,
            related_field_name="task_id", pulled_field_name="project_team_id"
        )
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: task.Task,
            related_field_name="task_id", pulled_field_name="dedicated_team_id"
        )
        company_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: task.Task,
            related_field_name="task_id", pulled_field_name="company_id"
        )

        system_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: system_change_request.SystemChangeRequest, related_field_name="system_change_request_id", pulled_field_name="system_id")
        system_has_function_points = cubista.PullByForeignPrimaryKeyField(lambda: system.System, related_field_name="system_id", pulled_field_name="has_function_points")

        planning_period_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: change_request.ChangeRequest,
            related_field_name="change_request_id",
            pulled_field_name="planning_period_id"
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

        kind_id = cubista.ForeignKeyField(foreign_table=lambda: FunctionComponentKind, default=-1, nulls=False)
        kind_function_points = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: FunctionComponentKind, related_field_name="kind_id", pulled_field_name="function_points")
        count = cubista.IntField(nulls=False)
        function_points = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["is_cancelled"] or not x["system_has_function_points"] else x["count"] * x["kind_function_points"],
            source_fields=["count", "kind_function_points", "is_cancelled", "system_has_function_points"]
        )

class FunctionComponentKind(cubista.Table):
    INPUT = 1
    OUTPUT = 2
    TABLE = 3
    MESSAGE = 4
    INTERFACE = 5

    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        function_points = cubista.IntField()
import cubista
from . import state
from . import task

class FunctionComponent(cubista.Table):
    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default=-1, nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        task_id = cubista.ForeignKeyField(foreign_table=lambda: task.Task, default="-1", nulls=False)
        kind_id = cubista.ForeignKeyField(foreign_table=lambda: FunctionComponentKind, default=-1, nulls=False)
        kind_function_points = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: FunctionComponentKind, related_field_name="kind_id", pulled_field_name="function_points")
        count = cubista.IntField(nulls=False)
        function_points = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["count"] * x["kind_function_points"],
            source_fields=["count", "kind_function_points"]
        )

class FunctionComponentKind(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
        function_points = cubista.IntField()
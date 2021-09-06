import cubista
from . import system
from . import change_request
from . import state
from . import task
import pandas as pd

class SystemChangeRequest(cubista.Table):
    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        url = cubista.StringField()
        name = cubista.StringField()
        system_id = cubista.ForeignKeyField(foreign_table=lambda: system.System, default=-1, nulls=False)
        analysis_preliminary_estimate = cubista.FloatField(nulls=True)
        development_preliminary_estimate = cubista.FloatField(nulls=True)
        testing_preliminary_estimate = cubista.FloatField(nulls=True)
        analysis_planned_estimate = cubista.FloatField(nulls=True)
        development_planned_estimate = cubista.FloatField(nulls=True)
        testing_planned_estimate = cubista.FloatField(nulls=True)
        state_id = cubista.ForeignKeyField(foreign_table=lambda: state.State, default=-1, nulls=False)
        state_category_id = cubista.PullByForeignPrimaryKeyField(lambda: state.State, related_field_name="state_id", pulled_field_name="category_id")
        change_request_id = cubista.ForeignKeyField(foreign_table=lambda: change_request.ChangeRequest, default="-1", nulls=False)
        project_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="project_team_id")
        dedicated_team_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="dedicated_team_id")
        company_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="company_id")

        has_value = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="has_value")
        planning_period_id = cubista.PullByForeignPrimaryKeyField(foreign_table=lambda: change_request.ChangeRequest, related_field_name="change_request_id", pulled_field_name="planning_period_id")

        analysis_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_tasks_estimate_sum = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="testing_estimate",
            aggregate_function="sum",
            default=0
        )

        tasks_estimate_sum = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_tasks_estimate_sum"] + x["development_tasks_estimate_sum"] + x["testing_tasks_estimate_sum"],
            source_fields=["analysis_tasks_estimate_sum", "development_tasks_estimate_sum", "testing_tasks_estimate_sum"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: task.Task,
            foreign_field_name="system_change_request_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        time_spent = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] + x["development_time_spent"] + x["testing_time_spent"],
            source_fields=["analysis_time_spent", "development_time_spent", "testing_time_spent"]
        )

        analysis_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["analysis_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["analysis_planned_estimate"] if not pd.isnull(x["analysis_planned_estimate"]) else (
                            x["analysis_preliminary_estimate"] if not pd.isnull(x["analysis_preliminary_estimate"]) else 0
                        ),
                        x["analysis_tasks_estimate_sum"],
                        x["analysis_time_spent"]
                    )
                ),
            source_fields=["analysis_time_spent", "state_category_id", "analysis_planned_estimate", "analysis_preliminary_estimate", "analysis_tasks_estimate_sum"]
        )

        development_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["development_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["development_planned_estimate"] if not pd.isnull(x["development_planned_estimate"]) else (
                            x["development_preliminary_estimate"] if not pd.isnull(x["development_preliminary_estimate"]) else 0
                        ),
                        x["development_tasks_estimate_sum"],
                        x["development_time_spent"]
                    )
                ),
            source_fields=["development_time_spent", "state_category_id", "development_planned_estimate", "development_preliminary_estimate", "development_tasks_estimate_sum"]
        )

        testing_estimate = cubista.CalculatedField(
            lambda_expression=lambda x:
                x["testing_time_spent"] if x["state_category_id"] == state.StateCategory.DONE else (
                    max(
                        x["testing_planned_estimate"] if not pd.isnull(x["testing_planned_estimate"]) else (
                            x["testing_preliminary_estimate"] if not pd.isnull(x["testing_preliminary_estimate"]) else 0
                        ),
                        x["testing_tasks_estimate_sum"],
                        x["testing_time_spent"]
                    )
                ),
            source_fields=["testing_time_spent", "state_category_id", "testing_planned_estimate", "testing_preliminary_estimate", "testing_tasks_estimate_sum"]
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

class SystemChangeRequestTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: task.TaskTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["date"])
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="change_request_id"
        )

class SystemChangeRequestAnalysisTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: task.TaskAnalysisTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["date"])
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="change_request_id"
        )

class SystemChangeRequestDevelopmentTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: task.TaskDevelopmentTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["date"])
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="change_request_id"
        )

class SystemChangeRequestTestingTimeSheetByDate(cubista.AggregatedTable):
    class Aggregation:
        source = lambda: task.TaskTestingTimeSheetByDate
        sort_by: [str] = ["date"]
        group_by: [str] = ["system_change_request_id", "date"]
        filter = None
        filter_fields: [str] = []

    class Fields:
        id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
        system_change_request_id = cubista.AggregatedTableGroupField(source="system_change_request_id")
        date = cubista.AggregatedTableGroupField(source="date")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")
        time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["system_change_request_id"], sort_by=["date"])
        change_request_id = cubista.PullByForeignPrimaryKeyField(
            foreign_table=lambda: SystemChangeRequest,
            related_field_name="system_change_request_id",
            pulled_field_name="change_request_id"
        )
import cubista
import datetime
from . import change_request

class PlanningPeriod(cubista.Table):
    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.CalculatedField(lambda_expression=lambda x:
                str(x["id"]) if x["id"] != -1 else "Не указано",
            source_fields=["id"]
        )

        start = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 1, 1) if x["id"] != -1 else datetime.date(2100, 1, 1),
            source_fields=["id"]
        )

        end = cubista.CalculatedField(
            lambda_expression=lambda x:
                datetime.date(x["id"], 12, 31) if x["id"] != -1 else datetime.date(2100, 1, 1),
            source_fields=["id"]
        )

        analysis_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="analysis_time_spent",
            aggregate_function="sum",
            default=0
        )

        development_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="development_time_spent",
            aggregate_function="sum",
            default=0
        )

        testing_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="testing_time_spent",
            aggregate_function="sum",
            default=0
        )

        management_time_spent = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
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
            foreign_field_name="planning_period_id",
            aggregated_field_name="analysis_estimate",
            aggregate_function="sum",
            default=0
        )

        development_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="development_estimate",
            aggregate_function="sum",
            default=0
        )

        testing_estimate = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
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
            foreign_field_name="planning_period_id",
            aggregated_field_name="function_points",
            aggregate_function="sum",
            default=0
        )

        function_points_effort = cubista.AggregatedForeignField(
            foreign_table=lambda: change_request.ChangeRequest,
            foreign_field_name="planning_period_id",
            aggregated_field_name="function_points_effort",
            aggregate_function="sum",
            default=0
        )

        effort_per_function_point = cubista.CalculatedField(
            lambda_expression=lambda x: 0 if x["function_points"] == 0 else x["function_points_effort"] / x["function_points"],
            source_fields=["function_points_effort", "function_points"]
        )
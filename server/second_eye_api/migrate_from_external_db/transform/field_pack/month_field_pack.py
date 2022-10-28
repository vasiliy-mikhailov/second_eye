import cubista
import datetime

from .. import utils

class MonthFieldPack(cubista.FieldPack):
    class Fields:
        month = cubista.CalculatedField(
            lambda_expression=lambda x: datetime.date(x["date"].year, x["date"].month, 1),
            source_fields=["date"]
        )

        working_days_in_month_occured = cubista.CalculatedField(
            lambda_expression=lambda x: utils.working_days_in_month_occured(for_date=x["month"], sys_date=datetime.date.today()),
            source_fields=["month"]
        )

        analysis_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["analysis_time_spent", "working_days_in_month_occured"]
        )

        development_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["development_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["development_time_spent", "working_days_in_month_occured"]
        )

        testing_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["testing_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["testing_time_spent", "working_days_in_month_occured"]
        )

        management_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["management_time_spent", "working_days_in_month_occured"]
        )

        incident_fixing_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["incident_fixing_time_spent", "working_days_in_month_occured"]
        )

        non_project_activity_time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["non_project_activity_time_spent", "working_days_in_month_occured"]
        )

        time_spent_month_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] / 8 / x["working_days_in_month_occured"] if x["working_days_in_month_occured"] else 0,
            source_fields=["time_spent", "working_days_in_month_occured"]
        )

class MonthFieldPackForAggregatedTable(cubista.FieldPack):
    class Fields:
        analysis_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="analysis_time_spent_month_fte", aggregate_function="sum")
        development_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="development_time_spent_month_fte", aggregate_function="sum")
        testing_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="testing_time_spent_month_fte", aggregate_function="sum")
        management_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="management_time_spent_month_fte", aggregate_function="sum")
        incident_fixing_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_month_fte", aggregate_function="sum")
        non_project_activity_time_spent_month_fte = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_month_fte", aggregate_function="sum")
        time_spent_month_fte = cubista.AggregatedTableAggregateField(source="time_spent_month_fte", aggregate_function="sum")

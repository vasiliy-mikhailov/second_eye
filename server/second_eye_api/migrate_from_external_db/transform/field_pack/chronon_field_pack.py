import cubista
import datetime

from .. import utils

class ChrononFieldPackForNormalTable(cubista.FieldPack):
    class Fields:
        is_in_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: utils.is_in_chronon_bounds(for_date=x["date"], sys_date=datetime.date.today()),
            source_fields=["date"]
        )

        analysis_time_spent_chronon = cubista.CalculatedField(lambda_expression=lambda x:
            x["analysis_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["analysis_time_spent", "is_in_chronon"]
        )

        analysis_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["analysis_time_spent_chronon"] / 160,
            source_fields=["analysis_time_spent_chronon"]
        )

        development_time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["development_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["development_time_spent", "is_in_chronon"]
        )

        development_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["development_time_spent_chronon"] / 160,
            source_fields=["development_time_spent_chronon"]
        )

        testing_time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["testing_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["testing_time_spent", "is_in_chronon"]
        )

        testing_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["testing_time_spent_chronon"] / 160,
            source_fields=["testing_time_spent_chronon"]
        )

        management_time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["management_time_spent", "is_in_chronon"]
        )

        management_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["management_time_spent_chronon"] / 160,
            source_fields=["management_time_spent_chronon"]
        )

        incident_fixing_time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["incident_fixing_time_spent", "is_in_chronon"]
        )

        incident_fixing_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["incident_fixing_time_spent_chronon"] / 160,
            source_fields=["incident_fixing_time_spent_chronon"]
        )

        non_project_activity_time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["non_project_activity_time_spent", "is_in_chronon"]
        )

        non_project_activity_time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["non_project_activity_time_spent_chronon"] / 160,
            source_fields=["non_project_activity_time_spent_chronon"]
        )

        time_spent_chronon = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent"] if x["is_in_chronon"] else 0,
            source_fields=["time_spent", "is_in_chronon"]
        )

        time_spent_chronon_fte = cubista.CalculatedField(
            lambda_expression=lambda x: x["time_spent_chronon"] / 160,
            source_fields=["time_spent_chronon"]
        )


        chronon_start_date = cubista.CalculatedField(
            lambda_expression=lambda x: utils.chronon_start_date(
                sys_date=datetime.date.today(),
            ),
            source_fields=[]
        )

        chronon_end_date = cubista.CalculatedField(
            lambda_expression=lambda x: utils.chronon_end_date(
                sys_date=datetime.date.today(),
            ),
            source_fields=[]
        )


class ChrononFieldPackForAggregatedTable(cubista.FieldPack):
    class Fields:
        analysis_time_spent_chronon = cubista.AggregatedTableAggregateField(source="analysis_time_spent_chronon", aggregate_function="sum")
        development_time_spent_chronon = cubista.AggregatedTableAggregateField(source="development_time_spent_chronon", aggregate_function="sum")
        testing_time_spent_chronon = cubista.AggregatedTableAggregateField(source="testing_time_spent_chronon", aggregate_function="sum")
        management_time_spent_chronon = cubista.AggregatedTableAggregateField(source="management_time_spent_chronon", aggregate_function="sum")
        incident_fixing_time_spent_chronon = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_chronon", aggregate_function="sum")
        non_project_activity_time_spent_chronon = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_chronon", aggregate_function="sum")
        time_spent_chronon = cubista.AggregatedTableAggregateField(source="time_spent_chronon", aggregate_function="sum")

        analysis_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="analysis_time_spent_chronon_fte", aggregate_function="sum")
        development_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="development_time_spent_chronon_fte", aggregate_function="sum")
        testing_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="testing_time_spent_chronon_fte", aggregate_function="sum")
        management_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="management_time_spent_chronon_fte", aggregate_function="sum")
        incident_fixing_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent_chronon_fte", aggregate_function="sum")
        non_project_activity_time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent_chronon_fte", aggregate_function="sum")
        time_spent_chronon_fte = cubista.AggregatedTableAggregateField(source="time_spent_chronon_fte", aggregate_function="sum")

        chronon_start_date = cubista.CalculatedField(
            lambda_expression=lambda x: utils.chronon_start_date(
                sys_date=datetime.date.today(),
            ),
            source_fields=[]
        )

        chronon_end_date = cubista.CalculatedField(
            lambda_expression=lambda x: utils.chronon_end_date(
                sys_date=datetime.date.today(),
            ),
            source_fields=[]
        )


class ChrononFieldPackAsAggregatedForeignFields:
    def __init__(self, foreign_table, foreign_field_name):
        self.foreign_table = foreign_table
        self.foreign_field_name = foreign_field_name


    def apply_to_table(self, table):
        foreign_table = self.foreign_table
        foreign_field_name = self.foreign_field_name

        time_spent_field_names = [
            "analysis_time_spent_chronon",
            "development_time_spent_chronon",
            "testing_time_spent_chronon",
            "management_time_spent_chronon",
            "incident_fixing_time_spent_chronon",
            "non_project_activity_time_spent_chronon",
            "time_spent_chronon",
            "analysis_time_spent_chronon_fte",
            "development_time_spent_chronon_fte",
            "testing_time_spent_chronon_fte",
            "management_time_spent_chronon_fte",
            "incident_fixing_time_spent_chronon_fte",
            "non_project_activity_time_spent_chronon_fte",
            "time_spent_chronon_fte",
        ]

        table_fields = table.Fields

        for time_spent_field_name in time_spent_field_names:
            field_object = cubista.AggregatedForeignField(
                foreign_table=foreign_table,
                foreign_field_name=foreign_field_name,
                aggregated_field_name=time_spent_field_name,
                aggregate_function="sum",
                default=0
            )

            setattr(table_fields, time_spent_field_name, field_object)

        setattr(
            table_fields,
            "chronon_start_date",
            cubista.CalculatedField(
                lambda_expression=lambda x: utils.chronon_start_date(
                    sys_date=datetime.date.today(),
                ),
                source_fields=[]
            )
        )

        setattr(
            table_fields,
            "chronon_end_date",
            cubista.CalculatedField(
                lambda_expression=lambda x: utils.chronon_end_date(
                    sys_date=datetime.date.today(),
                ),
                source_fields=[]
            )
        )
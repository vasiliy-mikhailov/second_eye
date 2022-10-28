import cubista

class TimeSpentFieldPackForAggregatedTable(cubista.FieldPack):
    class Fields:
        analysis_time_spent = cubista.AggregatedTableAggregateField(source="analysis_time_spent", aggregate_function="sum")
        development_time_spent = cubista.AggregatedTableAggregateField(source="development_time_spent", aggregate_function="sum")
        testing_time_spent = cubista.AggregatedTableAggregateField(source="testing_time_spent", aggregate_function="sum")
        management_time_spent = cubista.AggregatedTableAggregateField(source="management_time_spent", aggregate_function="sum")
        incident_fixing_time_spent = cubista.AggregatedTableAggregateField(source="incident_fixing_time_spent", aggregate_function="sum")
        non_project_activity_time_spent = cubista.AggregatedTableAggregateField(source="non_project_activity_time_spent", aggregate_function="sum")
        time_spent = cubista.AggregatedTableAggregateField(source="time_spent", aggregate_function="sum")

class TimeSpentFieldPackAsAggregatedForeignFields:
    def __init__(self, foreign_table, foreign_field_name):
        self.foreign_table = foreign_table
        self.foreign_field_name = foreign_field_name

    def apply_to_table(self, table):
        foreign_table = self.foreign_table
        foreign_field_name = self.foreign_field_name

        field_names = [
            "analysis_time_spent",
            "development_time_spent",
            "testing_time_spent",
            "management_time_spent",
            "incident_fixing_time_spent",
            "non_project_activity_time_spent",
            "time_spent"
        ]

        table_fields = table.Fields

        for field_name in field_names:
            field_object = cubista.AggregatedForeignField(
                foreign_table=foreign_table,
                foreign_field_name=foreign_field_name,
                aggregated_field_name=field_name,
                aggregate_function="sum",
                default=0
            )

            setattr(table_fields, field_name, field_object)
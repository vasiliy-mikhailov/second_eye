import cubista
from cubista import Table

class ModelInputField(Field):
    def __init__(self, source, primary_key=False):
        super(ModelInputField, self).__init__()
        self.source = source
        self.primary_key = primary_key

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_ready_to_be_evaluated(self):
        return False

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_calculation(self):
        return True

    def is_ready_to_be_used_in_calculation(self):
        table = self.table
        data_source = table.data_source
        source_table_type = table.Model.source()
        source_table = data_source.tables[source_table_type]
        source_field_name = self.source
        source_field_object = source_table.Fields.__dict__[source_field_name]

        return source_field_object.is_evaluated()

class PlanningPeriodTimeSheetModelTable(Table):
    class Model:
        source = None
        group_by = None
    class Fields:
        date = ModelInputField("date")
        planning_period_start = ModelInputField("planning_period_start")
        planning_period_end = ModelInputField("planning_period_end")
        time_spent_cumsum = ModelInputField("time_spent_cumsum")
        time_sheets_by_date_model_m = cubista.IntField("time_sheets_by_date_model_m")
        time_sheets_by_date_model_b = cubista.IntField("time_sheets_by_date_model_b")

    def __init__(self):
        data_frame = pd.DataFrame()
        super(PlanningPeriodTimeSheetModelTable, self).__init__(data_frame=data_frame)

    def are_fields_evaluated_in_source_table(self, field_names):
        source_table_type = self.Model.source()
        data_source = self.data_source

        source_table = data_source.tables[source_table_type]

        for field_name in field_names:
            field_object = source_table.Fields.__dict__[field_name]

            if not field_object.is_evaluated():
                return False

        return True

    def are_fields_required_for_creating_model_evaluated_in_source_table(self):
        fields = [self.group_by, "date", "planning_period_start", "planning_period_end", ]

        for field_name, field_object in fields.items():
            if field_object.is_required_for_aggregation() and not field_object.is_ready_to_be_aggregated():
                return False

        return True

    def is_ready_to_be_aggregated(self):
        sort_by_field_names = self.Aggregation.sort_by

        if not self.are_fields_evaluated_in_source_table(field_names=sort_by_field_names):
            return False

        group_by_field_names = self.Aggregation.group_by

        if not self.are_fields_evaluated_in_source_table(field_names=group_by_field_names):
            return False

        filter_fields = self.Aggregation.filter_fields

        if not self.are_fields_evaluated_in_source_table(field_names=filter_fields):
            return False

        if not self.are_fields_required_for_aggregation_evaluated_in_source_table():
            return False

        return True

    def get_aggregated_field_name_to_aggregate_function_mapping(self):
        fields = self.get_fields()

        result = {}

        for field_name, field_object in fields.items():
            if isinstance(field_object, cubista.AggregatedTableAggregateField):
                source_field = field_object.source
                aggregate_function = field_object.aggregate_function
                result[field_name] = (source_field, aggregate_function)

        return result

    def get_aggregated_source_field_name_to_destination_field_name_mapping(self):
        fields = self.get_fields()

        result = {}

        for field_name, field_object in fields.items():
            if isinstance(field_object, cubista.AggregatedTableGroupField) or isinstance(field_object, cubista.AggregatedTableAggregateField):
                source_field = field_object.source
                result[source_field] = field_name

        return result

    def get_group_source_field_name_to_destination_field_name_mapping(self):
        fields = self.get_fields()

        result = {}

        for field_name, field_object in fields.items():
            if isinstance(field_object, cubista.AggregatedTableGroupField):
                source_field = field_object.source
                result[source_field] = field_name

        return result

    def calculate(self):
        source_table_type = self.Model.source()
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]

        source_table_filtered_by_period_start_and_end = source_table[
            (source_table["date"] >= source_table[
                "planning_period_start"])
            & (source_table["date"] <= source_table[
                "planning_period_end"])
            ]

        model = source_table_filtered_by_period_start_and_end.groupby(
            ["planning_period_id"]
        ).apply(lambda x: pd.Series(
            linear_polyfit(
                x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
                y=x["time_spent_cumsum"]),
            index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        ))

        new_data_frame = new_data_frame.rename(columns=group_source_field_name_to_destination_field_name_mapping)

        primary_key_field_name = self.get_primary_key_field_name()

        new_data_frame[primary_key_field_name] = new_data_frame.apply(
            lambda x: -x.name - 2,
            axis=1
        )

        self.data_frame = new_data_frame

    def evaluate(self):
        is_ready_to_be_calculated = self.is_ready_to_be_calculated()

        if is_ready_to_be_calculated:
            self.calculate()

        super(PlanningPeriodTimeSheetModelTable, self).evaluate()
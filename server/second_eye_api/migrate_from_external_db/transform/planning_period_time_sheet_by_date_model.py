import cubista
from cubista import Table, Field
import pandas as pd
import numpy as np

def linear_polyfit(x, y):
    try:
        non_nan_indexes = np.isfinite(x) & np.isfinite(y)
        non_nan_x, non_nan_y = x[non_nan_indexes], y[non_nan_indexes]
        result = np.polyfit(non_nan_x, non_nan_y, 1, w=y).tolist()
        return result
    except:
        return [float("nan"), float("nan")]

class PeriodIdField(Field):
    def __init__(self, source):
        super(PeriodIdField, self).__init__()
        self.source = source
        self.primary_key = True

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

class ModelOutputField(Field):
    def __init__(self, source):
        super(ModelOutputField, self).__init__()
        self.source = source
        self.primary_key = False

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

class ModelTable(Table):
    class Model:
        source = None
        planning_period_id_field_name = None

    def __init__(self):
        data_frame = pd.DataFrame()
        super(ModelTable, self).__init__(data_frame=data_frame)
        self.date_field_name = "date"
        self.planning_period_start_field_name = "planning_period_start"
        self.planning_period_end_field_name = "planning_period_end"
        self.time_spent_cumsum_field_name = "time_spent_cumsum"

    def are_fields_evaluated_in_source_table(self, field_names):
        source_table_type = self.Model.source()
        data_source = self.data_source

        source_table = data_source.tables[source_table_type]

        for field_name in field_names:
            field_object = source_table.Fields.__dict__[field_name]

            if not field_object.is_evaluated():
                return False

        return True

    def is_ready_to_be_calculated(self):
        planning_period_id_field_name = self.Model.planning_period_id_field_name
        date_field_name = self.date_field_name
        planning_period_start_field_name = self.planning_period_start_field_name
        planning_period_end_field_name = self.planning_period_end_field_name
        time_spent_cumsum_field_name = self.time_spent_cumsum_field_name
        field_names = [planning_period_id_field_name, date_field_name, planning_period_start_field_name, planning_period_end_field_name, time_spent_cumsum_field_name]

        return self.are_fields_evaluated_in_source_table(field_names=field_names)

    def calculate(self):
        source_table_type = self.Model.source()
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]

        planning_period_id_field_name = self.Model.planning_period_id_field_name
        date_field_name = self.date_field_name
        planning_period_start_field_name = self.planning_period_start_field_name
        planning_period_end_field_name = self.planning_period_end_field_name
        time_spent_cumsum_field_name = self.time_spent_cumsum_field_name
        source_data_frame = source_table.data_frame

        source_data_frame_filtered_by_period_start_and_end = source_data_frame[
            (source_data_frame[date_field_name] >= source_data_frame[
                planning_period_start_field_name])
            & (source_data_frame[date_field_name] <= source_data_frame[
                planning_period_end_field_name])
            ]

        model = source_data_frame_filtered_by_period_start_and_end.groupby(
            [planning_period_id_field_name]
        ).apply(lambda x: pd.Series(
            linear_polyfit(
                x=(x[date_field_name] - x[planning_period_start_field_name]) / (x[planning_period_end_field_name] - x[planning_period_start_field_name]),
                y=x[time_spent_cumsum_field_name]),
            index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
        )).reset_index()

        self.data_frame = model

    def evaluate(self):
        is_ready_to_be_calculated = self.is_ready_to_be_calculated()

        if is_ready_to_be_calculated:
            self.calculate()

        super(ModelTable, self).evaluate()
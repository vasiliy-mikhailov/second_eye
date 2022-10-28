import cubista
import pandas as pd
import numpy as np
import warnings
import datetime
warnings.simplefilter('ignore', np.RankWarning)

def linear_polyfit(x, y):
    min_x = x.min()
    max_x = x.max()
    normalized_x = (x - min_x) / (max_x - min_x)

    non_nan_indexes = np.isfinite(normalized_x) & np.isfinite(y)
    non_nan_x, non_nan_y = normalized_x[non_nan_indexes], y[non_nan_indexes]

    has_x_values = not non_nan_x.empty

    if has_x_values:
        weights = y ** 2
        m, b = np.polyfit(x=non_nan_x, y=non_nan_y, deg=1, w=weights).tolist()
        if not min_x:
            min_x = datetime.date.today()

        if not max_x:
            max_x = datetime.date.today()

        result = [m, b, min_x, max_x]
    else:
        m, b = [0.0, 0.0]
        result = [m, b, datetime.date.today(), datetime.date.today()]

    return result

class EntityIdField(cubista.Field):
    def __init__(self, source):
        super(EntityIdField, self).__init__()
        self.source = source
        self.primary_key = True

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
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

class ModelOutputField(cubista.Field):
    def __init__(self, source):
        super(ModelOutputField, self).__init__()
        self.source = source
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
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

class ModelTable(cubista.Table):
    class Model:
        source = None
        entity_id_field_name = None

    def __init__(self):
        data_frame = pd.DataFrame()
        super(ModelTable, self).__init__(data_frame=data_frame)
        self.date_field_name = "date"
        self.time_spent_cumsum_field_name = "time_spent_cumsum"
        self.time_sheets_by_date_model_m_field_name = "time_sheets_by_date_model_m"
        self.time_sheets_by_date_model_b_field_name = "time_sheets_by_date_model_b"
        self.time_sheets_by_date_model_min_date_field_name = "time_sheets_by_date_model_min_date"
        self.time_sheets_by_date_model_max_date_field_name = "time_sheets_by_date_model_max_date"

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
        entity_id_field_name = self.Model.entity_id_field_name
        date_field_name = self.date_field_name
        time_spent_cumsum_field_name = self.time_spent_cumsum_field_name
        field_names = [entity_id_field_name, date_field_name, time_spent_cumsum_field_name]

        return self.are_fields_evaluated_in_source_table(field_names=field_names)

    def calculate(self):
        source_table_type = self.Model.source()
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]

        entity_id_field_name = self.Model.entity_id_field_name
        date_field_name = self.date_field_name
        time_spent_cumsum_field_name = self.time_spent_cumsum_field_name
        source_data_frame = source_table.data_frame
        source_data_frame_grouped_by_entity_id_field_name = source_data_frame.groupby(
            [entity_id_field_name],
            as_index=False
        )

        time_sheets_by_date_model_min_date_field_name = self.time_sheets_by_date_model_min_date_field_name
        time_sheets_by_date_model_max_date_field_name = self.time_sheets_by_date_model_max_date_field_name
        time_sheets_by_date_model_m_field_name = self.time_sheets_by_date_model_m_field_name
        time_sheets_by_date_model_b_field_name = self.time_sheets_by_date_model_b_field_name

        model = source_data_frame_grouped_by_entity_id_field_name.apply(
            lambda x: pd.Series(
                linear_polyfit(
                    x=x[date_field_name],
                    y=x[time_spent_cumsum_field_name],
                ),
                index=[time_sheets_by_date_model_m_field_name, time_sheets_by_date_model_b_field_name, time_sheets_by_date_model_min_date_field_name, time_sheets_by_date_model_max_date_field_name]
            )
        ) if source_data_frame_grouped_by_entity_id_field_name.ngroups else pd.DataFrame({
            entity_id_field_name: pd.Series(dtype=type(entity_id_field_name)),
            time_sheets_by_date_model_m_field_name: pd.Series(dtype=float),
            time_sheets_by_date_model_b_field_name: pd.Series(dtype=float),
            time_sheets_by_date_model_min_date_field_name: pd.Series(dtype='datetime64[ns]'),
            time_sheets_by_date_model_max_date_field_name: pd.Series(dtype='datetime64[ns]')
        })

        self.data_frame = model

    def evaluate(self):
        is_ready_to_be_calculated = self.is_ready_to_be_calculated()

        if is_ready_to_be_calculated:
            self.calculate()

        super(ModelTable, self).evaluate()
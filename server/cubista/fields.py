import datetime
import time

import cubista
from .exceptions import *
import pandas as pd

class Field:
    def __init__(self):
        self.name = ''
        self.table = None

    def check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            self,
            data,
            unique
    ):
        name = self.name
        for _, value in data.items():
            self.check_value_fits_field_raise_exception_otherwise(value=value)

        if unique:
            counts = data.value_counts()
            repeating_values = counts[counts > 1].index.to_list()
            if repeating_values:
                raise NonUniqueValuesFound("Field {} must have unique values, but has repeating value(s): {}.".format(str(self), repeating_values))

    def check_value_fits_field_raise_exception_otherwise(self, value):
        raise NotImplementedError

    def __str__(self):
        name = self.name
        table = self.table
        return "{}.{}".format(type(table), name)

class IntField(Field):
    def __init__(self, nulls=False, unique=False, primary_key=False):
        super(IntField, self).__init__()
        if primary_key and not unique:
            raise PrimaryKeyMustBeUnique()

        if primary_key and nulls:
            raise PrimaryKeyCannotHaveNulls

        self.nulls = nulls
        self.unique = unique
        self.primary_key = primary_key

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            unique=unique
        )

    def check_value_fits_field_raise_exception_otherwise(self, value):
        nulls = self.nulls
        required_types = [int, float]

        if not nulls and pd.isnull(value):
            raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

        data_type = type(value)
        if value and (data_type not in required_types):
            raise FieldTypeMismatch(
                "Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

    def is_evaluated(self):
        return True

    def do_nothing_intentionally(self):
        pass

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_required_for_aggregation(self):
        return False

class StringField(Field):
    def __init__(self, nulls=False, unique=False, primary_key=False):
        super(StringField, self).__init__()
        if primary_key and not unique:
            raise PrimaryKeyMustBeUnique()

        if primary_key and nulls:
            raise PrimaryKeyCannotHaveNulls

        self.nulls = nulls
        self.unique = unique
        self.primary_key = primary_key

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            unique=unique
        )

    def check_value_fits_field_raise_exception_otherwise(self, value):
        nulls = self.nulls
        required_types = [str]

        if not nulls and pd.isnull(value):
            raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

        data_type = type(value)
        if value and (data_type not in required_types):
            raise FieldTypeMismatch(
                "Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

    def do_nothing_intentionally(self):
        pass

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_evaluated(self):
        return True

    def is_required_for_aggregation(self):
        return False

class FloatField(Field):
    def __init__(self, nulls=False, unique=False, primary_key=False):
        super(FloatField, self).__init__()
        if primary_key and not unique:
            raise PrimaryKeyMustBeUnique()

        if primary_key and nulls:
            raise PrimaryKeyCannotHaveNulls

        self.nulls = nulls
        self.unique = unique
        self.primary_key = primary_key

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            unique=unique
        )

    def check_value_fits_field_raise_exception_otherwise(self, value):
        nulls = self.nulls
        required_types = [float, int]

        if not nulls and pd.isnull(value):
            raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

        data_type = type(value)
        if value and (data_type not in required_types):
            raise FieldTypeMismatch(
                "Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

    def do_nothing_intentionally(self):
        pass

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_evaluated(self):
        return True

    def is_required_for_aggregation(self):
        return False

class BoolField(Field):
    def __init__(self, nulls=False, unique=False, primary_key=False):
        super(BoolField, self).__init__()
        if primary_key and not unique:
            raise PrimaryKeyMustBeUnique()

        if primary_key and nulls:
            raise PrimaryKeyCannotHaveNulls

        self.nulls = nulls
        self.unique = unique
        self.primary_key = primary_key

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            unique=unique
        )

    def check_value_fits_field_raise_exception_otherwise(self, value):
        nulls = self.nulls
        required_types = [bool]

        if not nulls and pd.isnull(value):
            raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

        data_type = type(value)
        if value and (data_type not in required_types):
            raise FieldTypeMismatch(
                "Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

    def do_nothing_intentionally(self):
        pass

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_evaluated(self):
        return True

    def is_required_for_aggregation(self):
        return False

class DateField(Field):
    def __init__(self, nulls=False, unique=False, primary_key=False):
        super(DateField, self).__init__()
        if primary_key and not unique:
            raise PrimaryKeyMustBeUnique()

        if primary_key and nulls:
            raise PrimaryKeyCannotHaveNulls

        self.nulls = nulls
        self.unique = unique
        self.primary_key = primary_key

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            unique=unique
        )

    def check_value_fits_field_raise_exception_otherwise(self, value):
        nulls = self.nulls
        required_types = [datetime.date, pd._libs.tslibs.nattype.NaTType]

        if not nulls and pd.isnull(value):
            raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

        data_type = type(value)
        if value and (data_type not in required_types):
            raise FieldTypeMismatch(
                "Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

    def do_nothing_intentionally(self):
        pass

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_evaluated(self):
        return True

    def is_required_for_aggregation(self):
        return False

class ForeignKeyField(Field):
    def __init__(self, foreign_table, default, nulls=False):
        super(ForeignKeyField, self).__init__()
        self.foreign_table = foreign_table
        self.default = default
        self.nulls = nulls
        self.primary_key = False
        self.references_checked = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
        self.do_nothing_intentionally()

    def check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(self, table, field_name, foreign_table, foreign_field_name, value):
        field_object = foreign_table.get_field_by_name(field_name=foreign_field_name)

        try:
            field_object.check_value_fits_field_raise_exception_otherwise(value=value)
        except FieldTypeMismatch as e:
            raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))
        except NullsNotAllowed as e:
            raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))

    def check_references_raise_exception_otherwise(self):
        table = self.table

        data_frame = table.data_frame

        field_name = self.name

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        default_value_for_referencing_nowhere = self.default

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        foreign_table_primary_key_field_name = foreign_table.get_primary_key_field_name()

        self.check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(
            table=table,
            field_name=field_name,
            foreign_table=foreign_table,
            foreign_field_name=foreign_table_primary_key_field_name,
            value=default_value_for_referencing_nowhere
        )

        foreign_primary_key_values = foreign_table.data_frame[foreign_table_primary_key_field_name].dropna().unique()

        data_frame[field_name] = data_frame[field_name].where(data_frame[field_name].isin(foreign_primary_key_values), default_value_for_referencing_nowhere)

        self.references_checked = True

    def is_evaluated(self):
        return self.references_checked

    def is_required_for_aggregation(self):
        return False

class PullByForeignPrimaryKeyField(Field):
    def __init__(self, foreign_table, related_field_name, pulled_field_name):
        super(PullByForeignPrimaryKeyField, self).__init__()
        self.foreign_table = foreign_table
        self.related_field_name = related_field_name
        self.pulled_field = pulled_field_name
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def get_foreign_table(self):
        table = self.table

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        return foreign_table

    def is_related_field_evaluated(self):
        related_field_name = self.related_field_name
        table = self.table
        data_frame = table.data_frame
        columns = data_frame.columns
        return related_field_name in columns

    def is_pulled_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        pulled_field = self.pulled_field
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return pulled_field in foreign_columns

    def is_ready_to_be_evaluated(self):
        if not self.is_related_field_evaluated():
            return False

        if not self.is_pulled_field_evaluated():
            return False

        return True

    def evaluate(self):
        pulled_field = self.pulled_field
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        foreign_table = self.get_foreign_table()
        foreign_table_primary_key_field_name = foreign_table.get_primary_key_field_name()

        reduced_foreign_data_frame = foreign_table.data_frame[[foreign_table_primary_key_field_name, pulled_field]]\
            .set_index(foreign_table_primary_key_field_name)\
            .rename(columns={ pulled_field: field_name })

        related_field_name = self.related_field_name

        new_data_frame = data_frame.merge(
            reduced_foreign_data_frame,
            how="left",
            left_on=related_field_name,
            right_index=True,
            suffixes=(None, "")
        )

        table.data_frame = new_data_frame

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

class PullByRelatedField(Field):
    def __init__(self, foreign_table, related_field_names, foreign_field_names, pulled_field_name, default):
        super(PullByRelatedField, self).__init__()
        self.foreign_table = foreign_table
        self.related_field_names = related_field_names
        self.foreigh_field_names = foreign_field_names
        self.pulled_field = pulled_field_name
        self.default = default
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def get_foreign_table(self):
        table = self.table

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        return foreign_table

    def are_related_fields_evaluated(self):
        related_field_names = self.related_field_names
        table = self.table
        data_frame = table.data_frame
        columns = data_frame.columns
        result = all(related_field_name in columns for related_field_name in related_field_names)
        return result

    def are_foreign_fields_evaluated(self):
        foreign_table = self.get_foreign_table()
        foreign_field_names = self.foreigh_field_names
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        result = all(foreign_field_name in foreign_columns for foreign_field_name in foreign_field_names)
        return result

    def is_pulled_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        pulled_field_name = self.pulled_field
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return pulled_field_name in foreign_columns

    def is_ready_to_be_evaluated(self):
        if not self.are_related_fields_evaluated():
            return False

        if not self.are_foreign_fields_evaluated():
            return False

        if not self.is_pulled_field_evaluated():
            return False

        return True

    def check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(self, table, field_name, foreign_table, pulled_field, value):
        field_object = foreign_table.get_field_by_name(field_name=pulled_field)

        try:
            field_object.check_value_fits_field_raise_exception_otherwise(value=value)
        except FieldTypeMismatch as e:
            raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))
        except NullsNotAllowed as e:
            raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))

    def evaluate(self):
        pulled_field = self.pulled_field
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        related_field_names = self.related_field_names
        foreign_table = self.get_foreign_table()

        foreign_field_names = self.foreigh_field_names

        default = self.default

        self.check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(
            table=table,
            field_name=field_name,
            foreign_table=foreign_table,
            pulled_field=pulled_field,
            value=default
        )

        reduced_foreign_data_frame = foreign_table.data_frame[foreign_field_names + [pulled_field]]\
            .set_index(foreign_field_names)\
            .rename(columns={ pulled_field: field_name })

        data_frame_with_merged_field = data_frame.merge(
            reduced_foreign_data_frame,
            how="left",
            left_on=related_field_names,
            right_index=True,
            suffixes=(None, "")
        )

        data_frame_with_merged_field[field_name].fillna(default, inplace=True)

        # pd.set_option('display.max_columns', None)
        # print("{}<-{}.{} on ({})=({}) during evaluation of {}".format(table, foreign_table, pulled_field, ",".join(related_field_names), ", ".join(foreign_field_names), self))
        # print(data_frame)
        # print(reduced_foreign_data_frame)
        # print(foreign_table.data_frame[foreign_field_names[0]].apply(type))
        # print(foreign_table.data_frame)

        data_frame[field_name] = data_frame_with_merged_field[field_name].values

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False


class CalculatedField(Field):
    def __init__(self, lambda_expression, source_fields):
        super(CalculatedField, self).__init__()
        self.lambda_expression = lambda_expression
        self.source_fields = source_fields
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
        table = self.table
        data_frame = table.data_frame
        columns = data_frame.columns

        source_fields = self.source_fields

        non_existent_fields = [source_field for source_field in source_fields if source_field not in columns]

        return len(non_existent_fields) == 0

    def evaluate(self):
        table = self.table
        data_frame = table.data_frame
        field_name = self.name
        lambda_expression = self.lambda_expression
        source_fields = self.source_fields

        data_frame[field_name] = data_frame[source_fields].apply(
            lambda_expression,
            axis=1,
            result_type="reduce"
        )

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

class AggregatedForeignField(Field):
    def __init__(self, foreign_table, foreign_field_name, aggregated_field_name, aggregate_function, default):
        super(AggregatedForeignField, self).__init__()
        self.foreign_table = foreign_table
        self.foreign_field_name = foreign_field_name
        self.aggregated_field_name = aggregated_field_name
        self.aggregate_function = aggregate_function
        self.default = default
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_primary_key_evaluated(self):
        table = self.table
        primary_key_field_name = table.get_primary_key_field_name()
        primary_key = table.get_field_by_name(field_name=primary_key_field_name)
        return primary_key.is_evaluated()

    def is_foreign_field_is_evaluated(self):
        table = self.table
        data_source = table.data_source
        foreign_table_type = self.foreign_table()
        foreign_table = data_source.tables[foreign_table_type]

        foreign_field_name = self.foreign_field_name
        foreign_field = foreign_table.get_field_by_name(field_name=foreign_field_name)
        return foreign_field.is_evaluated()

    def is_aggregated_field_evaluated(self):
        table = self.table
        data_source = table.data_source
        foreign_table_type = self.foreign_table()
        foreign_table = data_source.tables[foreign_table_type]

        aggregated_field_name = self.aggregated_field_name
        aggregated_field = foreign_table.get_field_by_name(field_name=aggregated_field_name)
        return aggregated_field.is_evaluated()

    def is_ready_to_be_evaluated(self):
        if not self.is_primary_key_evaluated():
            return False

        if not self.is_foreign_field_is_evaluated():
            return False

        if not self.is_aggregated_field_evaluated():
            return False

        return True

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

    def check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(self, table, field_name, foreign_table, aggregated_field, value):
        field_object = foreign_table.get_field_by_name(field_name=aggregated_field)

        try:
            field_object.check_value_fits_field_raise_exception_otherwise(value=value)
        except FieldTypeMismatch as e:
            raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))
        except NullsNotAllowed as e:
            raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))

    def evaluate(self):
        table = self.table
        data_source = table.data_source
        foreign_table_type = self.foreign_table()
        foreign_table = data_source.tables[foreign_table_type]

        foreign_field_name = self.foreign_field_name

        aggregated_field_name = self.aggregated_field_name
        aggregate_function = self.aggregate_function

        field_name = self.name

        default = self.default

        self.check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(
            table=table,
            field_name=field_name,
            foreign_table=foreign_table,
            aggregated_field=aggregated_field_name,
            value=default
        )

        reduced_foreign_data_frame = foreign_table.data_frame[[foreign_field_name, aggregated_field_name]]\
            .groupby(foreign_field_name)\
            .agg({ aggregated_field_name: aggregate_function })\
            .rename(columns={ aggregated_field_name: field_name })

        data_frame = table.data_frame

        primary_key_field_name = table.get_primary_key_field_name()

        data_frame_with_merged_field = data_frame.merge(
            reduced_foreign_data_frame,
            how="left",
            left_on=primary_key_field_name,
            right_index=True,
            suffixes=(None, "")
        )

        data_frame_with_merged_field[field_name].fillna(default, inplace=True)

        data_frame[field_name] = data_frame_with_merged_field[field_name].values

class AggregatedTableAutoIncrementPrimaryKeyField(Field):
    def __init__(self):
        super(AggregatedTableAutoIncrementPrimaryKeyField, self).__init__()
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

    def is_required_for_aggregation(self):
        return False

    def apply_to_data_frame_after_aggregation_inplace(self, data_frame):
        field_name = self.name
        data_frame[field_name] = data_frame.apply(
            lambda x: -x.name - 2,
            axis=1,
            result_type="reduce"
        )


class AggregatedTableGroupField(Field):
    def __init__(self, source, primary_key=False):
        super(AggregatedTableGroupField, self).__init__()
        self.source = source
        self.primary_key = primary_key

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

    def is_required_for_aggregation(self):
        return True

    def is_ready_to_be_aggregated(self):
        table = self.table
        data_source = table.data_source
        source_table_type = table.Aggregation.source()
        source_table = data_source.tables[source_table_type]
        source_field_name = self.source

        if source_field_name in source_table.Fields.__dict__:
            source_field_object = source_table.Fields.__dict__[source_field_name]

            return source_field_object.is_evaluated()
        else:
            raise cubista.FieldDoesNotExist("Field {} not found in {} during evaluation of {}".format(source_field_name, source_table, self))

    def apply_to_data_frame_after_aggregation_inplace(self, data_frame):
        self.do_nothing_intentionally()

class AggregatedTableAggregateField(Field):
    def __init__(self, source, aggregate_function):
        super(AggregatedTableAggregateField, self).__init__()
        self.source = source
        self.aggregate_function = aggregate_function
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

    def is_required_for_aggregation(self):
        return True

    def is_ready_to_be_aggregated(self):
        table = self.table
        data_source = table.data_source
        source_table_type = table.Aggregation.source()
        source_table = data_source.tables[source_table_type]
        source_field_name = self.source

        if source_field_name in source_table.Fields.__dict__:
            source_field_object = source_table.Fields.__dict__[source_field_name]
        else:
            raise FieldDoesNotExist("Field {}.{} not found during evaluation of {}".format(source_table, source_field_name, self))

        return source_field_object.is_evaluated()

    def apply_to_data_frame_after_aggregation_inplace(self, data_frame):
        self.do_nothing_intentionally()

class CumSumField(Field):
    def __init__(self, source_field, group_by, sort_by):
        self.source_field = source_field
        self.group_by = group_by
        self.sort_by = sort_by
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def is_source_field_evaluated(self):
        source_field_name = self.source_field
        table = self.table
        data_frame = table.data_frame
        return source_field_name in data_frame.columns

    def is_group_by_fields_evaluated(self):
        group_by = self.group_by
        table = self.table
        data_frame = table.data_frame
        return all([group_by_field in data_frame.columns for group_by_field in group_by])

    def is_sort_by_fields_evaluated(self):
        sort_by = self.sort_by
        table = self.table
        data_frame = table.data_frame
        return all([sort_by_field in data_frame.columns for sort_by_field in sort_by])

    def is_ready_to_be_evaluated(self):
        if not self.is_source_field_evaluated():
            return False

        if not self.is_group_by_fields_evaluated():
            return False

        if not self.is_sort_by_fields_evaluated():
            return False

        return True

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

    def evaluate(self):
        source_field_name = self.source_field
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        sort_by_field_names = self.sort_by
        group_by_field_names = self.group_by

        reduced_fields = [source_field_name] + group_by_field_names + sort_by_field_names

        new_data_frame = data_frame.sort_values(sort_by_field_names).reset_index(drop=True)

        new_data_frame[field_name] = new_data_frame.groupby(group_by_field_names)[source_field_name].cumsum(axis=0)

        table.data_frame = new_data_frame

class OuterJoinedTableTableAutoIncrementPrimaryKeyField():
    def __init__(self):
        super(OuterJoinedTableTableAutoIncrementPrimaryKeyField, self).__init__()
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

    def is_required_for_aggregation(self):
        return False

class OuterJoinedTableOuterJoinedField(Field):
    def __init__(self, source, default):
        super(OuterJoinedTableOuterJoinedField, self).__init__()
        self.source = source
        self.default = default
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

    def is_required_for_aggregation(self):
        return False


class PullMaxByRelatedField(Field):
    def __init__(self, foreign_table, related_field_names, foreign_field_names, max_field_name, pulled_field_name, default):
        super(PullMaxByRelatedField, self).__init__()
        self.foreign_table = foreign_table
        self.related_field_names = related_field_names
        self.foreigh_field_names = foreign_field_names
        self.max_field_name = max_field_name
        self.pulled_field_name = pulled_field_name
        self.default = default
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_value_fits_field_raise_exception_otherwise(self, value):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def get_foreign_table(self):
        table = self.table

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        return foreign_table

    def are_related_fields_evaluated(self):
        related_field_names = self.related_field_names
        table = self.table
        data_frame = table.data_frame
        columns = data_frame.columns
        result = all(field_name in columns for field_name in related_field_names)
        return result

    def are_foreign_fields_evaluated(self):
        foreign_table = self.get_foreign_table()
        foreign_field_names = self.foreigh_field_names
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        result = all(field_name in foreign_columns for field_name in foreign_field_names)
        return result

    def is_max_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        max_field_name = self.max_field_name
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return max_field_name in foreign_columns

    def is_pulled_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        pulled_field_name = self.pulled_field_name
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return pulled_field_name in foreign_columns

    def is_ready_to_be_evaluated(self):
        if not self.are_related_fields_evaluated():
            return False

        if not self.are_related_fields_evaluated():
            return False

        if not self.is_max_field_evaluated():
            return False

        if not self.is_pulled_field_evaluated():
            return False

        return True

    def check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(self, table, field_name, foreign_table, pulled_field, value):
        field_object = foreign_table.get_field_by_name(field_name=pulled_field)

        try:
            field_object.check_value_fits_field_raise_exception_otherwise(value=value)
        except FieldTypeMismatch as e:
            raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))
        except NullsNotAllowed as e:
            raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))

    def evaluate(self):
        max_field_name = self.max_field_name
        pulled_field_name = self.pulled_field_name
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        related_field_names = self.related_field_names
        foreign_table = self.get_foreign_table()

        foreign_field_names = self.foreigh_field_names

        default = self.default

        self.check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(
            table=table,
            field_name=field_name,
            foreign_table=foreign_table,
            pulled_field=pulled_field_name,
            value=default
        )

        reduced_foreign_data_frame = foreign_table.data_frame[foreign_field_names + [pulled_field_name, max_field_name]]\
            .reset_index()

        reduced_foreign_data_frame_with_deleted_non_max_row = reduced_foreign_data_frame.loc[
                reduced_foreign_data_frame.groupby(foreign_field_names)[max_field_name].idxmax()
            ]\
            .rename(columns={ pulled_field_name: field_name })

        reduced_foreign_data_frame_with_deleted_non_max_row_and_removed_max_field_from_columns = reduced_foreign_data_frame_with_deleted_non_max_row.drop(columns=[max_field_name])

        data_frame_with_merged_field = data_frame.merge(
            reduced_foreign_data_frame_with_deleted_non_max_row_and_removed_max_field_from_columns,
            how="left",
            left_on=related_field_names,
            right_on=foreign_field_names,
            suffixes=(None, "")
        )

        data_frame_with_merged_field[field_name].fillna(default, inplace=True)

        data_frame[field_name] = data_frame_with_merged_field[field_name].values

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

class PullMinByRelatedField(Field):
    def __init__(self, foreign_table, related_field_names, foreign_field_names, min_field_name, pulled_field_name, default):
        super(PullMinByRelatedField, self).__init__()
        self.foreign_table = foreign_table
        self.related_field_names = related_field_names
        self.foreigh_field_names = foreign_field_names
        self.min_field_name = min_field_name
        self.pulled_field_name = pulled_field_name
        self.default = default
        self.primary_key = False

    def do_nothing_intentionally(self):
        pass

    def check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(self, data):
        self.do_nothing_intentionally()

    def check_references_raise_exception_otherwise(self):
        self.do_nothing_intentionally()

    def get_foreign_table(self):
        table = self.table

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        return foreign_table

    def are_related_fields_evaluated(self):
        related_field_names = self.related_field_names
        table = self.table
        data_frame = table.data_frame
        columns = data_frame.columns
        result = all(field_name in columns for field_name in related_field_names)
        return result

    def are_foreign_fields_evaluated(self):
        foreign_table = self.get_foreign_table()
        foreign_field_names = self.foreigh_field_names
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        result = all(field_name in foreign_columns for field_name in foreign_field_names)
        return result

    def is_min_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        min_field_name = self.min_field_name
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return min_field_name in foreign_columns

    def is_pulled_field_evaluated(self):
        foreign_table = self.get_foreign_table()
        pulled_field_name = self.pulled_field_name
        foreign_data_frame = foreign_table.data_frame
        foreign_columns = foreign_data_frame.columns

        return pulled_field_name in foreign_columns

    def is_ready_to_be_evaluated(self):
        if not self.are_related_fields_evaluated():
            return False

        if not self.are_related_fields_evaluated():
            return False

        if not self.is_min_field_evaluated():
            return False

        if not self.is_pulled_field_evaluated():
            return False

        return True

    def check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(self, table, field_name, foreign_table, pulled_field, value):
        field_object = foreign_table.get_field_by_name(field_name=pulled_field)

        try:
            field_object.check_value_fits_field_raise_exception_otherwise(value=value)
        except FieldTypeMismatch as e:
            raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))
        except NullsNotAllowed as e:
            raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(value, type(value), table, field_name))

    def evaluate(self):
        min_field_name = self.min_field_name
        pulled_field_name = self.pulled_field_name
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        related_field_names = self.related_field_names
        foreign_table = self.get_foreign_table()

        foreign_field_names = self.foreigh_field_names

        default = self.default

        self.check_table_has_field_and_datatype_matches_value_raise_exception_otherwise(
            table=table,
            field_name=field_name,
            foreign_table=foreign_table,
            pulled_field=pulled_field_name,
            value=default
        )

        reduced_foreign_data_frame = foreign_table.data_frame[foreign_field_names + [pulled_field_name, min_field_name]]\
            .reset_index()

        reduced_foreign_data_frame_with_deleted_non_min_row = reduced_foreign_data_frame.loc[
                reduced_foreign_data_frame.groupby(foreign_field_names)[min_field_name].idxmin()
            ]\
            .rename(columns={ pulled_field_name: field_name })

        reduced_foreign_data_frame_with_deleted_non_min_row_and_removed_min_field_from_columns = reduced_foreign_data_frame_with_deleted_non_min_row.drop(columns=[min_field_name])

        data_frame_with_merged_field = data_frame.merge(
            reduced_foreign_data_frame_with_deleted_non_min_row_and_removed_min_field_from_columns,
            how="left",
            left_on=related_field_names,
            right_on=foreign_field_names,
            suffixes=(None, "")
        )

        data_frame_with_merged_field[field_name].fillna(default, inplace=True)

        data_frame[field_name] = data_frame_with_merged_field[field_name].values

    def is_evaluated(self):
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        return field_name in data_frame.columns

    def is_required_for_aggregation(self):
        return False

class UnionTableTableAutoIncrementPrimaryKeyField():
    def __init__(self):
        super(UnionTableTableAutoIncrementPrimaryKeyField, self).__init__()
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

    def is_required_for_aggregation(self):
        return False

class UnionTableUnionField(Field):
    def __init__(self, source):
        super(UnionTableUnionField, self).__init__()
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

    def is_required_for_aggregation(self):
        return False

import datetime
from .exceptions import *
import pandas as pd

class Field:
    def __init__(self):
        self.name = ''
        self.table = None

    def check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            self,
            data,
            required_types,
            nulls,
            unique
    ):
        name = self.name
        for _, value in data.items():
            if not nulls and pd.isnull(value):
                raise NullsNotAllowed("Field {} cannot contain nulls but null found.".format(str(self)))

            data_type = type(value)
            if value and (data_type not in required_types):
                raise FieldTypeMismatch("Field {} must have data type {}, but {} found.".format(str(self), required_types, data_type))

        if unique:
            counts = data.value_counts()
            repeating_values = counts[counts > 1].index.to_list()
            if repeating_values:
                raise NonUniqueValuesFound("Field {} must have unique values, but has repeating value(s): {}.".format(str(self), repeating_values))

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
        nulls = self.nulls
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            required_types=[int, float],
            nulls=nulls,
            unique=unique
        )

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
        nulls = self.nulls
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            required_types=[str],
            nulls=nulls,
            unique=unique
        )

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
        nulls = self.nulls
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            required_types=[float],
            nulls=nulls,
            unique=unique
        )

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
        nulls = self.nulls
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            required_types=[bool],
            nulls=nulls,
            unique=unique
        )

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
        nulls = self.nulls
        unique = self.unique
        self.check_field_data_type_nulls_and_uniqueness_in_data_frame_column_raise_exception_otherwise(
            data=data,
            required_types=[datetime.date, pd._libs.tslibs.nattype.NaTType],
            nulls=nulls,
            unique=unique
        )

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

    def check_references_raise_exception_otherwise(self):
        table = self.table

        data_frame = table.data_frame

        field_name = self.name

        foreign_table_type_lambda = self.foreign_table

        foreign_table_type = foreign_table_type_lambda()

        data_source = table.data_source

        foreign_table = data_source.tables[foreign_table_type]

        foreign_table_primary_key_field_name = foreign_table.get_primary_key_field_name()

        foreign_primary_key_values = foreign_table.data_frame[foreign_table_primary_key_field_name].dropna().unique()

        default_value_for_referencing_nowhere = self.default

        data_frame.loc[~data_frame[field_name].isin(foreign_primary_key_values), field_name] = default_value_for_referencing_nowhere

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

        if not self.are_related_fields_evaluated():
            return False

        if not self.is_pulled_field_evaluated():
            return False

        return True

    def evaluate(self):
        pulled_field = self.pulled_field
        field_name = self.name
        table = self.table
        data_frame = table.data_frame
        related_field_names = self.related_field_names
        foreign_table = self.get_foreign_table()

        foreign_field_names = self.foreigh_field_names

        reduced_foreign_data_frame = foreign_table.data_frame[foreign_field_names + [pulled_field]]\
            .set_index(foreign_field_names)\
            .rename(columns={ pulled_field: field_name })

        new_data_frame = data_frame.merge(
            reduced_foreign_data_frame,
            how="left",
            left_on=related_field_names,
            right_index=True,
            suffixes=(None, "")
        )

        default = self.default

        new_data_frame[field_name].fillna(default, inplace=True)

        table.data_frame = new_data_frame

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
            axis=1
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

    def evaluate(self):
        table = self.table
        data_source = table.data_source
        foreign_table_type = self.foreign_table()
        foreign_table = data_source.tables[foreign_table_type]

        foreign_field_name = self.foreign_field_name

        aggregated_field_name = self.aggregated_field_name
        aggregate_function = self.aggregate_function

        field_name = self.name

        reduced_foreign_data_frame = foreign_table.data_frame[[foreign_field_name, aggregated_field_name]]\
            .groupby(foreign_field_name)\
            .agg({ aggregated_field_name: aggregate_function })\
            .rename(columns={ aggregated_field_name: field_name })

        data_frame = table.data_frame

        primary_key_field_name = table.get_primary_key_field_name()

        new_data_frame = data_frame.merge(
            reduced_foreign_data_frame,
            how="left",
            left_on=primary_key_field_name,
            right_index=True,
            suffixes=(None, "")
        )

        default = self.default
        new_data_frame[field_name].fillna(default, inplace=True)

        table.data_frame = new_data_frame

class AggregatedTableAutoIncrementPrimaryKeyField(Field):
    def __init__(self):
        super(AggregatedTableAutoIncrementPrimaryKeyField, self).__init__()
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

class AggregatedTableGroupField(Field):
    def __init__(self, source, primary_key=False):
        super(AggregatedTableGroupField, self).__init__()
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

    def is_required_for_aggregation(self):
        return True

    def is_ready_to_be_aggregated(self):
        table = self.table
        data_source = table.data_source
        source_table_type = table.Aggregation.source()
        source_table = data_source.tables[source_table_type]
        source_field_name = self.source
        source_field_object = source_table.Fields.__dict__[source_field_name]

        return source_field_object.is_evaluated()

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
        source_field_object = source_table.Fields.__dict__[source_field_name]

        return source_field_object.is_evaluated()

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
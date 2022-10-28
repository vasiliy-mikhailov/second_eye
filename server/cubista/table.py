import cubista
from .exceptions import *
from . import fields as f
import pandas as pd
import time

class Table:
    class Fields:
        pass

    class FieldPacks:
        field_packs = []

    def __init__(self, data_frame):
        self.data_source = None
        self.data_frame = data_frame

        self.copy_fields_from_field_pack()
        self.set_field_names_and_table()

        self.check_all_not_evaluated_fields_exist_in_data_frame_and_raise_exception_otherwise()
        self.check_all_not_evaluated_fields_has_correct_data_type_in_data_frame_and_raise_exception_otherwise()
        self.check_only_one_primary_key_specified_and_raise_exception_otherwise()

    def get_field_by_name(self, field_name):
        return self.Fields.__dict__[field_name]

    def get_fields(self):
        return { key: value for key, value in self.Fields.__dict__.items() if not key.startswith("__") }

    def copy_fields_from_field_pack(self):
        field_packs = self.FieldPacks.field_packs

        for field_pack_lambda in field_packs:
            field_pack = field_pack_lambda()
            field_pack.apply_to_table(table=self)

    def set_field_names_and_table(self):
        fields = self.get_fields()
        for field_name, field_object in fields.items():
            field_object.name = field_name
            field_object.table = self

    def check_all_not_evaluated_fields_exist_in_data_frame_and_raise_exception_otherwise(self):
        fields = self.get_fields()
        data_frame = self.data_frame
        data_frame_columns = data_frame.columns

        for field_name, field_object in fields.items():
            if field_object.is_evaluated():
                if field_name not in data_frame_columns:
                    raise FieldDoesNotExist("Field {} not found in {}".format(field_name, ", ".join(data_frame_columns)))

    def check_all_not_evaluated_fields_has_correct_data_type_in_data_frame_and_raise_exception_otherwise(self):
        fields = self.get_fields()
        data_frame = self.data_frame

        for field_name, field_object in fields.items():
            if field_object.is_evaluated():
                data = data_frame[field_name]
                field_object.check_field_has_correct_data_type_in_data_frame_column_raise_exception_otherwise(data=data)

    def check_only_one_primary_key_specified_and_raise_exception_otherwise(self):
        fields = self.get_fields()

        primary_keys_count = sum([field_object.primary_key for _, field_object in fields.items()])

        if not primary_keys_count:
            raise cubista.NoPrimaryKeySpecified("No primary key specified in {}.".format(type(self)))

        if primary_keys_count > 1:
            raise cubista.MoreThanOnePrimaryKeySpecified("Only one primary key is allowed for {} but {} found.".format(type(self), primary_keys_count))

    def check_references_raise_exception_otherwise(self):
        fields = self.get_fields()

        for field_name, field_object in fields.items():
            field_object.check_references_raise_exception_otherwise()

    def get_primary_key_field(self):
        fields = self.get_fields()

        for field_name, field_object in fields.items():
            if field_object.primary_key:
                return field_object

    def get_primary_key_field_name(self):
        primary_key_field = self.get_primary_key_field()

        return primary_key_field.name

    def get_fields_to_evaluate(self, limited_fields_to_evaluate=None):
        fields_dictionary = self.get_fields()

        fields = [field_object for _, field_object in fields_dictionary.items()]

        not_evaluated_fields = [field for field in fields if not field.is_evaluated()]

        result = [field for field in not_evaluated_fields if field in limited_fields_to_evaluate] if limited_fields_to_evaluate else not_evaluated_fields

        return result

    def evaluate(self):
        fields_to_evaluate = self.get_fields_to_evaluate()

        for field_to_evaluate in fields_to_evaluate:
            if field_to_evaluate.is_ready_to_be_evaluated():
                start = time.time()
                field_to_evaluate.evaluate()
                end = time.time()
                duration = end - start

                # print("{} {}".format(duration, field_to_evaluate))


class AggregatedTable(Table):
    class Aggregation:
        source = None
        sort_by: [str] = []
        group_by: [str] = []
        filter = None
        filter_fields: [str] = []

    def __init__(self):
        self.already_aggregated = False
        data_frame = pd.DataFrame()
        super(AggregatedTable, self).__init__(data_frame=data_frame)

    def are_fields_evaluated_in_source_table(self, field_names):
        source_table_type = self.Aggregation.source()
        data_source = self.data_source

        source_table = data_source.tables[source_table_type]

        for field_name in field_names:
            if field_name in source_table.Fields.__dict__:
                field_object = source_table.Fields.__dict__[field_name]

                if not field_object.is_evaluated():
                    return False
            else:
                raise cubista.FieldDoesNotExist("Field {} not found in {} during evaluation of {}".format(field_name, source_table, self))

        return True

    def are_fields_required_for_aggregation_evaluated_in_source_table(self):
        fields = self.get_fields()

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

    def aggregate(self):
        start = time.time()

        source_table_type = self.Aggregation.source()
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]
        aggregated_source_field_name_to_destination_field_name_mapping = self.get_aggregated_source_field_name_to_destination_field_name_mapping()
        reduced_field_names = aggregated_source_field_name_to_destination_field_name_mapping.keys()
        sort_by_field_names = self.Aggregation.sort_by
        group_by_field_names = self.Aggregation.group_by
        new_data_frame = source_table.data_frame

        filter_fields = self.Aggregation.filter_fields
        filter = self.Aggregation.filter

        if filter_fields and filter:
            reduced_data_frame = source_table.data_frame[filter_fields]
            new_data_frame = new_data_frame[reduced_data_frame.apply(
                filter,
                axis=1,
                result_type="expand"
            )]

        new_data_frame = new_data_frame.sort_values(by=sort_by_field_names)
        new_data_frame = new_data_frame[reduced_field_names]
        new_data_frame = new_data_frame.groupby(group_by_field_names)
        aggregated_field_name_to_aggregate_function_mapping = self.get_aggregated_field_name_to_aggregate_function_mapping()

        new_data_frame = new_data_frame.agg(**aggregated_field_name_to_aggregate_function_mapping)

        new_data_frame = new_data_frame.reset_index()

        group_source_field_name_to_destination_field_name_mapping = self.get_group_source_field_name_to_destination_field_name_mapping()

        new_data_frame = new_data_frame.rename(columns=group_source_field_name_to_destination_field_name_mapping)

        primary_key_field = self.get_primary_key_field()

        primary_key_field.apply_to_data_frame_after_aggregation_inplace(data_frame=new_data_frame)

        self.data_frame = new_data_frame

        end = time.time()
        duration = end - start

        # print("******** {}".format(self))

    def evaluate(self):
        already_aggregated = self.already_aggregated

        if not already_aggregated:
            is_ready_to_be_aggregated = self.is_ready_to_be_aggregated()

            if is_ready_to_be_aggregated:
                self.aggregate()
                self.already_aggregated = True

        super(AggregatedTable, self).evaluate()


class OuterJoinedTable(Table):
    class OuterJoin:
        left_source_table = None
        right_source_table = None
        left_fields = {}
        right_fields = {}
        on_fields = []
        defaults = {}

    def __init__(self):
        self.already_joined = False
        data_frame = pd.DataFrame()
        super(OuterJoinedTable, self).__init__(data_frame=data_frame)

    def is_source_table_ready_to_be_evaluated(self, source_table_type, required_fields, limited_fields_to_evaluate=None):
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]

        required_field_names = required_fields.keys()

        not_evaluated_fields = source_table.get_fields_to_evaluate(limited_fields_to_evaluate=limited_fields_to_evaluate)

        required_not_evaluated_fields = [field for field in not_evaluated_fields if field.name in required_field_names]

        return len(required_not_evaluated_fields) == 0

    def is_ready_to_be_evaluated(self, limited_fields_to_evaluate=None):
        left_source_table_ready = self.is_source_table_ready_to_be_evaluated(
            source_table_type=self.OuterJoin.left_source_table(),
            required_fields=self.OuterJoin.left_fields,
            limited_fields_to_evaluate=limited_fields_to_evaluate
        )

        right_source_table_ready = self.is_source_table_ready_to_be_evaluated(
            source_table_type=self.OuterJoin.right_source_table(),
            required_fields=self.OuterJoin.right_fields,
            limited_fields_to_evaluate=limited_fields_to_evaluate
        )

        return left_source_table_ready and right_source_table_ready

    def check_table_has_fields_and_datatype_matches_value_raise_exception_otherwise(self, table, fields, outer_joined_fields):
        renamed_fields = list(fields.values())
        original_fields = list(fields.keys())

        for field_name, field_object in outer_joined_fields.items():
            default_value = field_object.default

            if field_name in renamed_fields:
                source_field_index = renamed_fields.index(field_name)
                source_field_name = original_fields[source_field_index]
                original_field_object = table.get_field_by_name(field_name=source_field_name)

                try:
                    original_field_object.check_value_fits_field_raise_exception_otherwise(value=default_value)
                except FieldTypeMismatch as e:
                    raise FieldTypeMismatch("Invalid value {} of type {} for field {}.{}".format(default_value, type(default_value), table, field_name))
                except NullsNotAllowed as e:
                    raise NullsNotAllowed("Invalid value {} of type {} for field {}.{}".format(default_value, type(default_value), table, field_name))

    def check_left_and_right_tables_has_fields_and_datatype_matches_value_raise_exception_otherwise(self, left_table, left_fields, right_table, right_fields, outer_joined_fields):
        self.check_table_has_fields_and_datatype_matches_value_raise_exception_otherwise(
            table=left_table,
            fields=left_fields,
            outer_joined_fields=outer_joined_fields
        )

        self.check_table_has_fields_and_datatype_matches_value_raise_exception_otherwise(
            table=right_table,
            fields=right_fields,
            outer_joined_fields=outer_joined_fields
        )

    def join(self):
        left_table_type = self.OuterJoin.left_source_table()
        data_source = self.data_source
        left_table = data_source.tables[left_table_type]
        left_fields = self.OuterJoin.left_fields
        left_field_names = left_fields.keys()

        reduced_left_data_frame = left_table.data_frame[left_field_names] \
            .rename(columns=left_fields)

        right_table_type = self.OuterJoin.right_source_table()
        right_table = data_source.tables[right_table_type]
        right_fields = self.OuterJoin.right_fields
        right_field_names = right_fields.keys()

        fields = self.get_fields()

        outer_joined_fields = {field_name: field_object for field_name, field_object in fields.items() if
                               isinstance(field_object, f.OuterJoinedTableOuterJoinedField)}

        self.check_left_and_right_tables_has_fields_and_datatype_matches_value_raise_exception_otherwise(
            left_table=left_table,
            left_fields=left_fields,
            right_table=right_table,
            right_fields=right_fields,
            outer_joined_fields=outer_joined_fields
        )

        reduced_right_data_frame = right_table.data_frame[right_field_names] \
            .rename(columns=right_fields)

        on_fields = self.OuterJoin.on_fields

        if not on_fields:
            reduced_left_data_frame["__artificial_temporary_index"] = 1
            reduced_right_data_frame["__artificial_temporary_index"] = 1

            outer_joined_data_frame = reduced_left_data_frame.merge(
                reduced_right_data_frame,
                how="outer",
                on=["__artificial_temporary_index"],
                suffixes=(None, "")
            )

            outer_joined_data_frame.drop('__artificial_temporary_index', axis=1, inplace=True)
        else:
            outer_joined_data_frame = reduced_left_data_frame.merge(
                reduced_right_data_frame,
                how="outer",
                on=on_fields,
                suffixes=(None, "")
            )

        primary_key_field_name = self.get_primary_key_field_name()

        outer_joined_data_frame[primary_key_field_name] = outer_joined_data_frame.apply(
            lambda x: -x.name - 2,
            axis=1,
            result_type="reduce"
        )

        for field_name, field_object in outer_joined_fields.items():
            default_value = field_object.default

            outer_joined_data_frame[field_name].fillna(default_value, inplace=True)

        self.data_frame = outer_joined_data_frame

    def evaluate(self):
        already_joined = self.already_joined

        if not already_joined:
            is_ready_to_be_evaluated = self.is_ready_to_be_evaluated()

            if is_ready_to_be_evaluated:
                start = time.time()
                self.join()
                self.already_joined = True
                end = time.time()
                duration = end - start

                # print("******** {}".format(self))

        super(OuterJoinedTable, self).evaluate()

class UnionTable(Table):
    class Union:
        tables: [] = []
        fields: [str] = []

    def __init__(self):
        self.already_united = False
        data_frame = pd.DataFrame()
        super(UnionTable, self).__init__(data_frame=data_frame)

    def is_source_table_ready_to_be_evaluated(self, source_table_type, fields, limited_fields_to_evaluate=None):
        data_source = self.data_source
        source_table = data_source.tables[source_table_type]

        not_evaluated_fields = source_table.get_fields_to_evaluate(limited_fields_to_evaluate=limited_fields_to_evaluate)

        not_evaluated_fields = [field for field in not_evaluated_fields if field.name in fields]

        return len(not_evaluated_fields) == 0

    def is_ready_to_be_evaluated(self, limited_fields_to_evaluate=None):
        tables = self.Union.tables
        fields = self.Union.fields

        for table_lambda in tables:
            table = table_lambda()
            if not self.is_source_table_ready_to_be_evaluated(
                source_table_type=table,
                fields=fields
            ):
                return False

        return True

    def make_reduced_data_frame(self, source_table_type, fields):
        data_source = self.data_source
        table = data_source.tables[source_table_type]

        reduced_data_frame = table.data_frame[fields]

        return reduced_data_frame

    def union(self):
        tables = self.Union.tables
        fields = self.Union.fields

        reduced_data_frames = []

        for table_lambda in tables:
            table = table_lambda()
            reduced_data_frame = self.make_reduced_data_frame(
                source_table_type=table,
                fields=fields
            )

            reduced_data_frames.append(reduced_data_frame)

        union_data_frame = pd.concat(
            reduced_data_frames,
            ignore_index=True
        )

        primary_key_field_name = self.get_primary_key_field_name()

        union_data_frame[primary_key_field_name] = union_data_frame.apply(
            lambda x: -x.name - 2,
            axis=1,
            result_type="reduce"
        )

        # pd.set_option('display.max_columns', None)
        # print(union_data_frame)

        self.data_frame = union_data_frame

    def evaluate(self, limited_fields_to_evaluate=None):
        already_united = self.already_united

        if not already_united:
            is_ready_to_be_evaluated = self.is_ready_to_be_evaluated()

            if is_ready_to_be_evaluated:
                start = time.time()
                self.union()
                self.already_united = True
                end = time.time()
                duration = end - start

                # print("******** {}".format(self))

        super(UnionTable, self).evaluate()
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
import graphene
import math

class DataFrameObjectType_Meta(SubclassWithMeta_Meta):
    def __new__(meta, class_name, bases, class_attributes):
        if "Fields" in class_attributes:
            fields_attributes = class_attributes["Fields"]
            for field_name, field_value in fields_attributes.__dict__.items():
                if isinstance(field_value, FieldType):
                    field_type_class = field_value
                    field_type_class.modify_class_attributes(
                        class_name=class_name,
                        class_attributes=class_attributes,
                        field_name=field_name,
                        field_value=field_value
                    )

        return type.__new__(meta, class_name, bases, class_attributes)

class FieldType:
    def modify_class_attributes(self, class_name, class_attributes, field_attributes):
        raise NotImplementedError()

def resolve_lambda_if_needed(lambda_or_object):
    if callable(lambda_or_object):
        lambda_or_object = lambda_or_object()

    return lambda_or_object

class PrimaryKey(FieldType):
    def __init__(self, field_type):
        self.field_type = field_type

    @classmethod
    def find_primary_key_in_entity(cls, entity):
        class_attributes = entity.__dict__
        return cls.find_primary_key_in_class_attributes(class_attributes=class_attributes)

    @classmethod
    def find_primary_key_in_class_attributes(clc, class_attributes):
        if "Fields" in class_attributes:
            fields_class = class_attributes["Fields"]

            fields = fields_class.__dict__

            for field_name, field_value in fields.items():
                if isinstance(field_value, PrimaryKey):
                    return field_name


    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        underlying_field_type = field_value.field_type
        underlying_field_type.modify_class_attributes(
            class_name=class_name,
            class_attributes=class_attributes,
            field_name=field_name,
            field_value=field_value
        )

class String(FieldType):
    def __init__(self, nulls=False, unique=False):
        self.nulls = nulls
        self.unique = unique

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        class_attributes[field_name] = graphene.String()

class Int(FieldType):
    def __init__(self, nulls=False, unique=False):
        self.nulls = nulls
        self.unique = unique

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        class_attributes[field_name] = graphene.Int()

class Float(FieldType):
    def __init__(self, nulls=False, unique=False):
        self.nulls = nulls
        self.unique = unique

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        class_attributes[field_name] = graphene.Float()

class Date(FieldType):
    def __init__(self, nulls=False, unique=False):
        self.nulls = nulls
        self.unique = unique

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        class_attributes[field_name] = graphene.Date()

class Boolean(FieldType):
    def __init__(self, nulls=False, unique=False):
        self.nulls = nulls
        self.unique = unique

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        class_attributes[field_name] = graphene.Boolean()

class Field(FieldType):
    def __init__(self, foreign_entity):
        self.foreign_entity = foreign_entity

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        field_name_with_id = field_name + "_id"

        foreign_entity = field_value.foreign_entity
        class_attributes[field_name] = graphene.Field(foreign_entity)
        class_attributes["resolve_{}".format(field_name)] = lambda self, _: \
            resolve_lambda_if_needed(foreign_entity).get_by_primary_key_value(
                value=self[field_name_with_id],
                data_store=self['data_store']
            )


class List(FieldType):
    def __init__(self, foreign_entity, to_field):
        self.foreign_entity = foreign_entity
        self.to_field = to_field

    def modify_class_attributes(self, class_name, class_attributes, field_name, field_value):
        self_primary_key_field_name = PrimaryKey.find_primary_key_in_class_attributes(class_attributes=class_attributes)
        to_field = field_value.to_field
        foreign_entity = field_value.foreign_entity

        class_attributes[field_name] = graphene.List(field_value.foreign_entity)

        class_attributes["resolve_{}".format(field_name)] = lambda self, _: \
            resolve_lambda_if_needed(foreign_entity).filter(
                field=to_field,
                value=self[self_primary_key_field_name],
                data_store=self['data_store']
            )

class DataFrameObjectType(graphene.ObjectType, metaclass=DataFrameObjectType_Meta):
    @classmethod
    def get_indexed_data_frame_make_if_needed(cls, field, data_store):
        return data_store.get_indexed_data_frame_make_if_needed(data_frame_object_type=cls, field=field)

    @classmethod
    def fix_value_for_graphene(cls, value):
        if type(value) is float and math.isnan(value):
            return None

        return value

    @classmethod
    def convert_data_frame_to_dict_adding_data_store(cls, data_frame, data_store):
        return [dict(
            [(colname, cls.fix_value_for_graphene(row[i])) for i, colname in enumerate(data_frame.columns)]
            + [('data_store', data_store)]
        ) for row in data_frame.values]

    @classmethod
    def all(cls, data_store):
        data_frame = data_store.data_frames[cls]
        return cls.convert_data_frame_to_dict_adding_data_store(data_frame=data_frame, data_store=data_store)

    @classmethod
    def get_by_field_value(cls, field, value, data_store):
        filtered_values = cls.filter(field, value, data_store)

        number_of_record_found = len(filtered_values)

        if number_of_record_found != 1:
            raise ValueError("{} expected exactly 1 record with {}={} but {} found {}.".format(cls, field, value, number_of_record_found, filtered_values))

        single_record = filtered_values[0]

        return single_record

    @classmethod
    def get_by_primary_key_value(cls, value, data_store):
        primary_key_field_name = PrimaryKey.find_primary_key_in_entity(entity=cls)

        return cls.get_by_field_value(field=primary_key_field_name, value=value, data_store=data_store)

    @classmethod
    def filter(cls, field, value, data_store):
        data_frame = cls.get_indexed_data_frame_make_if_needed(field, data_store)
        filtered_data_frame = data_frame.loc[[value]]

        return cls.convert_data_frame_to_dict_adding_data_store(data_frame=filtered_data_frame, data_store=data_store)

class DataStore:
    def __init__(self, data_frames):
        self.data_frames = data_frames
        self.indexed_data_frames = {}
        self.check_integrity()

    def check_integrity(self):
        pass

    def get_indexed_data_frame_make_if_needed(self, data_frame_object_type, field):
        indexed_data_frames = self.indexed_data_frames

        if data_frame_object_type not in indexed_data_frames:
            indexed_data_frames[data_frame_object_type] = {}


        if field not in indexed_data_frames[data_frame_object_type]:
            data_frames = self.data_frames
            data_frame = data_frames[data_frame_object_type]
            indexed_data_frames[data_frame_object_type][field] = data_frame.set_index(field, drop=False)

        return indexed_data_frames[data_frame_object_type][field]

import pytest
import cubista
import pandas as pd
import datetime

def test_when_field_has_int_type_but_data_frame_has_not_int_data_type_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField()

    data = {
        "id": ["Wrong", "Datatype"]
    }

    data_frame = pd.DataFrame(data)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_data_frame_has_int_data_type_without_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(nulls=False, unique=True, primary_key=True)

    data = {
        "id": [1, 2]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_data_frame_has_int_data_type_with_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [1, 2, None],
        "pk": [1, 2, 3]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_is_required_but_data_frame_has_nulls_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField()

    data_with_nulls = {
        "id": [1, 2, None]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    with pytest.raises(cubista.NullsNotAllowed):
        _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_is_not_required_and_data_frame_has_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_nulls = {
        "id": [1, 2, None],
        "pk": [1, 2, 3]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_requires_unique_but_value_repeats_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(unique=True)

    data_with_repeating_values = {
        "id": [1, 2, 2]
    }

    data_frame = pd.DataFrame(data_with_repeating_values)

    with pytest.raises(cubista.NonUniqueValuesFound):
        _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_requires_unique_and_null_value_repeats_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(nulls=True, unique=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_repeating_nulls = {
        "id": [1, 2, None, None],
        "pk": [1, 2, 3, 4]
    }

    data_frame = pd.DataFrame(data_with_repeating_nulls)

    _ = Table(data_frame=data_frame)

def test_when_field_has_int_type_and_primary_key_and_not_unique_raises_exception():
    with pytest.raises(cubista.PrimaryKeyMustBeUnique):
        class _(cubista.Table):
            class Fields:
                id = cubista.IntField(unique=False, primary_key=True)

def test_when_field_has_int_type_and_primary_key_and_allows_nulls_raises_exception():
    with pytest.raises(cubista.PrimaryKeyCannotHaveNulls):
        class _(cubista.Table):
            class Fields:
                id = cubista.IntField(unique=True, primary_key=True, nulls=True)

def test_when_field_has_string_type_but_data_frame_has_not_object_data_type_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.StringField()

    data_with_wrong_data_types = {
        "id": [1, 2]
    }

    data_frame = pd.DataFrame(data_with_wrong_data_types)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = Table(data_frame=data_frame)

def test_when_field_has_string_type_and_data_frame_has_object_data_type_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.StringField()
            pk = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": ["Correct", "data"],
        "pk": [1, 2]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_string_type_and_does_not_allow_nulls_but_data_frame_has_nulls_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.StringField()

    data = {
        "id": ["Correct", "data type", None]
    }

    data_frame = pd.DataFrame(data)

    with pytest.raises(cubista.NullsNotAllowed):
        _ = Table(data_frame=data_frame)

def test_when_field_has_string_type_and_allows_nulls_and_data_frame_has_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.StringField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_nulls = {
        "id": ["Correct", "data type", None],
        "pk": [1, 2, 3]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    _ = Table(data_frame=data_frame)

def test_when_field_has_string_type_and_requires_unique_but_value_repeats_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.StringField(unique=True)

    data_with_repeating_values = {
        "id": ["Hello", "Hello"]
    }

    data_frame = pd.DataFrame(data_with_repeating_values)

    with pytest.raises(cubista.NonUniqueValuesFound):
        _ = Table(data_frame=data_frame)

def test_when_field_has_string_type_and_primary_key_and_not_unique_raises_exception():
    with pytest.raises(cubista.PrimaryKeyMustBeUnique):
        class _(cubista.Table):
            class Fields:
                id = cubista.StringField(unique=False, primary_key=True)

def test_when_field_has_string_type_and_primary_key_and_allows_nulls_raises_exception():
    with pytest.raises(cubista.PrimaryKeyCannotHaveNulls):
        class _(cubista.Table):
            class Fields:
                id = cubista.StringField(unique=True, primary_key=True, nulls=True)

def test_when_field_has_float_type_but_data_frame_has_not_float64_data_type_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.FloatField()

    data_with_wrong_data_types = {
        "id": ["Wrong", "data type", None]
    }

    data_frame = pd.DataFrame(data_with_wrong_data_types)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = Table(data_frame=data_frame)

def test_when_field_has_float_type_and_data_frame_has_float64_data_type_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.FloatField()
            pk = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [3.1415, 2.718],
        "pk": [1, 2]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_float_type_and_does_not_allow_nulls_but_data_frame_has_nulls_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.FloatField()

    data = {
        "id": [3.14, 2.718, None]
    }

    data_frame = pd.DataFrame(data)

    with pytest.raises(cubista.NullsNotAllowed):
        _ = Table(data_frame=data_frame)

def test_when_field_has_float_type_and_allows_nulls_and_data_frame_has_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.FloatField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_nulls = {
        "id": [3.14, 2.718, None],
        "pk": [1, 2, 3]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    _ = Table(data_frame=data_frame)


def test_when_field_has_float_type_and_requires_unique_but_value_repeats_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.FloatField(unique=True)

    data_with_repeating_values = {
        "id": [1.0, 1.0]
    }

    data_frame = pd.DataFrame(data_with_repeating_values)

    with pytest.raises(cubista.NonUniqueValuesFound):
        _ = Table(data_frame=data_frame)

def test_when_field_has_float_type_and_primary_key_and_not_unique_raises_exception():
    with pytest.raises(cubista.PrimaryKeyMustBeUnique):
        class _(cubista.Table):
            class Fields:
                id = cubista.FloatField(unique=False, primary_key=True)

def test_when_field_has_float_type_and_primary_key_and_allows_nulls_raises_exception():
    with pytest.raises(cubista.PrimaryKeyCannotHaveNulls):
        class _(cubista.Table):
            class Fields:
                id = cubista.FloatField(unique=True, primary_key=True, nulls=True)

def test_when_field_has_bool_type_but_data_frame_has_not_bool_data_type_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.BoolField()

    data_with_wrong_data_types = {
        "id": ["Wrong", "data type", None]
    }

    data_frame = pd.DataFrame(data_with_wrong_data_types)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = Table(data_frame=data_frame)


def test_when_field_has_bool_type_and_data_frame_has_bool_data_type_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.BoolField()
            pk = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [True, False],
        "pk": [1, 2]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_bool_type_and_does_not_allow_nulls_but_data_frame_has_nulls_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.BoolField()

    data = {
        "id": [True, False, None]
    }

    data_frame = pd.DataFrame(data)

    with pytest.raises(cubista.NullsNotAllowed):
        _ = Table(data_frame=data_frame)

def test_when_field_has_bool_type_and_allows_nulls_and_data_frame_has_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.BoolField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_nulls = {
        "id": [True, False, None],
        "pk": [1, 2, 3]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    _ = Table(data_frame=data_frame)

def test_when_field_has_bool_type_and_requires_unique_but_value_repeats_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.BoolField(unique=True)

    data_with_repeating_values = {
        "id": [True, True]
    }

    data_frame = pd.DataFrame(data_with_repeating_values)

    with pytest.raises(cubista.NonUniqueValuesFound):
        _ = Table(data_frame=data_frame)

def test_when_field_has_bool_type_and_primary_key_and_not_unique_raises_exception():
    with pytest.raises(cubista.PrimaryKeyMustBeUnique):
        class _(cubista.Table):
            class Fields:
                id = cubista.BoolField(unique=False, primary_key=True)

def test_when_field_has_bool_type_and_primary_key_and_allows_nulls_raises_exception():
    with pytest.raises(cubista.PrimaryKeyCannotHaveNulls):
        class _(cubista.Table):
            class Fields:
                id = cubista.BoolField(unique=True, primary_key=True, nulls=True)

def test_when_field_has_date_type_but_data_frame_has_not_date_data_type_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.DateField()

    data_with_wrong_data_types = {
        "id": ["Wrong", None]
    }

    data_frame = pd.DataFrame(data_with_wrong_data_types)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = Table(data_frame=data_frame)

def test_when_field_has_date_type_and_data_frame_has_date_data_type_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.DateField()
            pk = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [datetime.date.today()],
        "pk": [1]
    }

    data_frame = pd.DataFrame(data)

    _ = Table(data_frame=data_frame)

def test_when_field_has_date_type_and_does_not_allow_nulls_but_data_frame_has_nulls_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.DateField()

    data = {
        "id": [datetime.date.today(), None]
    }

    data_frame = pd.DataFrame(data)

    with pytest.raises(cubista.NullsNotAllowed):
        _ = Table(data_frame=data_frame)

def test_when_field_has_date_type_and_allows_nulls_and_data_frame_has_nulls_does_not_raise_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.DateField(nulls=True)
            pk = cubista.IntField(primary_key=True, unique=True)

    data_with_nulls = {
        "id": [datetime.date.today(), None],
        "pk": [1, 2]
    }

    data_frame = pd.DataFrame(data_with_nulls)

    _ = Table(data_frame=data_frame)

def test_when_field_has_date_type_and_requires_unique_but_value_repeats_raises_exception():
    class Table(cubista.Table):
        class Fields:
            id = cubista.DateField(unique=True)

    data_with_repeating_values = {
        "id": [datetime.date.today(), datetime.date.today()]
    }

    data_frame = pd.DataFrame(data_with_repeating_values)

    with pytest.raises(cubista.NonUniqueValuesFound):
        _ = Table(data_frame=data_frame)

def test_when_field_has_date_type_and_primary_key_and_not_unique_raises_exception():
    with pytest.raises(cubista.PrimaryKeyMustBeUnique):
        class _(cubista.Table):
            class Fields:
                id = cubista.DateField(unique=False, primary_key=True)

def test_when_field_has_bool_type_and_primary_key_and_allows_nulls_raises_exception():
    with pytest.raises(cubista.PrimaryKeyCannotHaveNulls):
        class _(cubista.Table):
            class Fields:
                id = cubista.DateField(unique=True, primary_key=True, nulls=True)

def test_when_field_has_auto_increment_primary_key_type_it_has_attribute_primary_key_equals_true():
    class Table(cubista.AggregatedTable):
        class Fields:
            id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()

    table = Table()

    assert table.Fields.id.primary_key == True


def test_when_int_column_referenced_by_primary_key_and_default_is_string_exception_is_raised():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(lambda: Table1, default="-1")
            table1_name = cubista.PullByForeignPrimaryKeyField(lambda: Table1, related_field_name="table1_id", pulled_field_name="name")

    data1 = {
        "id": [1, 2],
        "name": ["one", "two"]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [100, 200],
        "table1_id": [1, 2]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2,
        ])

def test_when_column_pulled_by_primary_key_from_another_table_value_migrates():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(lambda: Table1, default=-1)
            table1_name = cubista.PullByForeignPrimaryKeyField(lambda: Table1, related_field_name="table1_id", pulled_field_name="name")

    data1 = {
        "id": [1, 2],
        "name": ["one", "two"]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [100, 200],
        "table1_id": [1, 2]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2,
    ])

    assert table2.data_frame["table1_name"].tolist() == ["one", "two"]

def test_when_string_column_pulled_by_related_field_from_another_table_and_default_is_int_exception_is_raised():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            first_id = cubista.IntField()
            second_id = cubista.IntField()
            table2_name = cubista.PullByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["first_id", "second_id"],
                foreign_field_names=["id1", "id2"],
                pulled_field_name="name",
                default=-1
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            id1 = cubista.IntField()
            id2 = cubista.IntField()
            name = cubista.StringField()

    data1 = {
        "id": [1, 2, 3],
        "first_id": [100, 200, 300],
        "second_id": [1000, 2000, 3000]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [-1, -2],
        "id1": [100, 200],
        "id2": [1000, 2000],
        "name": ["hello", "world"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2,
        ])

def test_when_column_pulled_by_related_field_from_another_table_value_migrates():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            first_id = cubista.IntField()
            second_id = cubista.IntField()
            table2_name = cubista.PullByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["first_id", "second_id"],
                foreign_field_names=["id1", "id2"],
                pulled_field_name="name", default="none"
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            id1 = cubista.IntField()
            id2 = cubista.IntField()
            name = cubista.StringField()

    data1 = {
        "id": [1, 2, 3],
        "first_id": [100, 200, 300],
        "second_id": [1000, 2000, 3000]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [-1, -2],
        "id1": [100, 200],
        "id2": [1000, 2000],
        "name": ["hello", "world"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2,
    ])

    assert table1.data_frame["first_id"].tolist() == [100, 200, 300]
    assert table1.data_frame["second_id"].tolist() == [1000, 2000, 3000]
    assert table1.data_frame["table2_name"].tolist() == ["hello", "world", "none"]

def test_when_string_field_pulled_by_max_has_int_default_value_raises_exception():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            pulled_description = cubista.PullMaxByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                max_field_name="value",
                pulled_field_name="description",
                default=-1
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2
        ])


def test_when_field_pulled_by_max_returns_max_value():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            pulled_description = cubista.PullMaxByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                max_field_name="value",
                pulled_field_name="description",
                default="-1"
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    resulting_table = table1.data_frame.sort_values(by=["id"])
    assert resulting_table.columns.tolist() == ["id", "pulled_description"]
    assert resulting_table["id"].tolist() == [1, 2, 3]
    assert resulting_table["pulled_description"].tolist() == ["two", "four", "-1"]

def test_when_columns_overlap_field_pulled_by_max_returns_max_value():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            value = cubista.FloatField()
            pulled_description = cubista.PullMaxByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                max_field_name="value",
                pulled_field_name="description",
                default="-1"
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3],
        "value": [1.0, 2.0, 3.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    resulting_table = table1.data_frame.sort_values(by=["id"])
    assert resulting_table.columns.tolist() == ["id", "value", "pulled_description"]
    assert resulting_table["id"].tolist() == [1, 2, 3]
    assert resulting_table["value"].tolist() == [1.0, 2.0, 3.0]
    assert resulting_table["pulled_description"].tolist() == ["two", "four", "-1"]

def test_when_string_field_pulled_by_min_has_default_int_value_raises_exception():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            pulled_description = cubista.PullMinByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                min_field_name="value",
                pulled_field_name="description",
                default=-1
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2
        ])

def test_when_field_pulled_by_min_returns_min_value():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            pulled_description = cubista.PullMinByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                min_field_name="value",
                pulled_field_name="description",
                default="-1"
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    resulting_table = table1.data_frame.sort_values(by=["id"])
    assert resulting_table.columns.tolist() == ["id", "pulled_description"]
    assert resulting_table["id"].tolist() == [1, 2, 3]
    assert resulting_table["pulled_description"].tolist() == ["one", "three", "-1"]

def test_when_columns_overlap_field_pulled_by_min_returns_min_value():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            value = cubista.FloatField()
            pulled_description = cubista.PullMinByRelatedField(
                foreign_table=lambda: Table2,
                related_field_names=["id"],
                foreign_field_names=["table1_id"],
                min_field_name="value",
                pulled_field_name="description",
                default="-1"
            )

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.IntField()
            value = cubista.FloatField()
            description = cubista.StringField()

    data1 = {
        "id": [1, 2, 3],
        "value": [1.0, 2.0, 3.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0],
        "description": ["one", "two", "three", "four"]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    resulting_table = table1.data_frame.sort_values(by=["id"])
    assert resulting_table.columns.tolist() == ["id", "value", "pulled_description"]
    assert resulting_table["id"].tolist() == [1, 2, 3]
    assert resulting_table["value"].tolist() == [1.0, 2.0, 3.0]
    assert resulting_table["pulled_description"].tolist() == ["one", "three", "-1"]

def test_aggregated_int_foreign_field_with_string_default_value_raises_exception():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            value_sum = cubista.AggregatedForeignField(lambda: Table2, foreign_field_name="table1_id", aggregated_field_name="value", aggregate_function="sum", default="incorrect")

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(foreign_table=lambda: Table1, default=-1, nulls=False)
            value = cubista.FloatField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2,
        ])

def test_aggregated_foreign_field_migrates_to_table():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            value_sum = cubista.AggregatedForeignField(lambda: Table2, foreign_field_name="table1_id", aggregated_field_name="value", aggregate_function="sum", default=0)

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(foreign_table=lambda: Table1, default=-1, nulls=False)
            value = cubista.FloatField()

    data1 = {
        "id": [1, 2, 3]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [10, 20, 30, 40],
        "table1_id": [1, 1, 2, 2],
        "value": [1.0, 2.0, 3.0, 4.0]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    assert table1.data_frame.columns.tolist() == ["id", "value_sum"]
    assert table1.data_frame["value_sum"].tolist() == [3.0, 7.0, 0.0]

def test_when_outer_join_left_table_int_joined_field_has_string_default_value_raises_exception():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key1_1 = cubista.IntField(nulls=True, unique=False)
            key1_2 = cubista.IntField(nulls=True, unique=False)
            plan_value = cubista.FloatField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key2_1 = cubista.IntField(nulls=True, unique=False)
            key2_2 = cubista.IntField(nulls=True, unique=False)
            fact_value = cubista.FloatField()

    class Table3(cubista.OuterJoinedTable):
        class OuterJoin:
            left_source_table: cubista.Table = lambda: Table1
            right_source_table: cubista.Table = lambda: Table2
            left_fields = {"key1_1": "key1", "key1_2": "key2", "plan_value": "plan_value"}
            right_fields = {"key2_1": "key1", "key2_2": "key2", "fact_value": "fact_value"}
            on_fields = ["key1", "key2"]

        class Fields:
            id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
            key1 = cubista.OuterJoinedTableOuterJoinedField(source="key1", default="incorrect")
            key2 = cubista.OuterJoinedTableOuterJoinedField(source="key2", default=-1)
            plan_value = cubista.OuterJoinedTableOuterJoinedField(source="plan_value", default=0)
            fact_value = cubista.OuterJoinedTableOuterJoinedField(source="fact_value", default=0)

    data1 = {
        "id": [1, 2],
        "key1_1": [10, 10],
        "key1_2": [20, 30],
        "plan_value": [1.0, 2.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [3, 4],
        "key2_1": [10, 10],
        "key2_2": [20, 40],
        "fact_value": [3.0, 4.0]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    table3 = Table3()

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2,
            table3
        ])

def test_when_outer_join_right_table_int_joined_field_has_string_default_value_raises_exception():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key1_1 = cubista.IntField(nulls=True, unique=False)
            key1_2 = cubista.IntField(nulls=True, unique=False)
            plan_value = cubista.FloatField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key2_1 = cubista.IntField(nulls=True, unique=False)
            key2_2 = cubista.IntField(nulls=True, unique=False)
            fact_value = cubista.FloatField()

    class Table3(cubista.OuterJoinedTable):
        class OuterJoin:
            left_source_table: cubista.Table = lambda: Table1
            right_source_table: cubista.Table = lambda: Table2
            left_fields = {"key1_1": "key1", "key1_2": "key2", "plan_value": "plan_value"}
            right_fields = {"key2_1": "key1", "key2_2": "key2", "fact_value": "fact_value"}
            on_fields = ["key1", "key2"]

        class Fields:
            id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
            key1 = cubista.OuterJoinedTableOuterJoinedField(source="key1", default=-1)
            key2 = cubista.OuterJoinedTableOuterJoinedField(source="key2", default="incorrect")
            plan_value = cubista.OuterJoinedTableOuterJoinedField(source="plan_value", default=0)
            fact_value = cubista.OuterJoinedTableOuterJoinedField(source="fact_value", default=0)

    data1 = {
        "id": [1, 2],
        "key1_1": [10, 10],
        "key1_2": [20, 30],
        "plan_value": [1.0, 2.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [3, 4],
        "key2_1": [10, 10],
        "key2_2": [20, 40],
        "fact_value": [3.0, 4.0]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    table3 = Table3()

    with pytest.raises(cubista.FieldTypeMismatch):
        _ = cubista.DataSource(tables=[
            table1,
            table2,
            table3
        ])



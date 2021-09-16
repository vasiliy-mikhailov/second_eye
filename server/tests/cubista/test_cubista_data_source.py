import pytest

import cubista
import pandas as pd
import datetime

def test_when_data_source_is_created_table_knows_its_data_source():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [1, 2]
    }
    data_frame = pd.DataFrame(data)

    table = Table(data_frame=data_frame)

    data_source = cubista.DataSource(tables=[table])

    assert table.data_source == data_source

def test_when_data_source_is_created_table_can_be_found_by_class_name():
    class Table(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)

    data = {
        "id": [1, 2]
    }
    data_frame = pd.DataFrame(data)

    table = Table(data_frame=data_frame)

    data_source = cubista.DataSource(tables=[table])

    assert data_source.tables[Table] == table

def test_when_column_referencing_primary_key_of_another_table_contains_value_not_from_that_primary_key_it_is_replaced_with_default_value():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(lambda: Table1, default=-1)

    data1 = {
        "id": [1, 2]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [100, 200],
        "table1_id": [3, 3]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    _ = cubista.DataSource(tables=[
        table1,
        table2,
    ])

    assert table2.data_frame["table1_id"].tolist() == [-1, -1]

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

def test_when_column_pulled_by_field_from_another_table_value_migrates():
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

def test_when_column_pulled_from_another_table_value_migrates_by_field_chain():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(lambda: Table1, default=-1)
            table1_name = cubista.PullByForeignPrimaryKeyField(lambda: Table1, related_field_name="table1_id", pulled_field_name="name")

    class Table3(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table2_id = cubista.ForeignKeyField(lambda: Table2, default=-1)
            table1_name = cubista.PullByForeignPrimaryKeyField(lambda: Table2, related_field_name="table2_id", pulled_field_name="table1_name")

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

    data3 = {
        "id": [300, 400],
        "table2_id": [1, 1]
    }
    data_frame3 = pd.DataFrame(data3)
    table3 = Table3(data_frame=data_frame3)

    _ = cubista.DataSource(tables=[
        table3,
        table2,
        table1,
    ])

    assert table2.data_frame["table1_name"].tolist() == ["one", "two"]

def test_when_column_cannot_be_pulled_from_another_table_exception_is_raised():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()

    class Table2MissedNameAttributeMigration(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table1_id = cubista.ForeignKeyField(lambda: Table1, default=-1)

    class Table3(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            table2_id = cubista.ForeignKeyField(lambda: Table2MissedNameAttributeMigration, default=-1)
            table1_name = cubista.PullByForeignPrimaryKeyField(lambda: Table2MissedNameAttributeMigration, related_field_name="table2_id", pulled_field_name="table1_name")

    data1 = {
        "id": [1, 2],
        "name": ["one", "two"]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [100, 200],
        "table1_id": [1, 1]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2MissedNameAttributeMigration(data_frame=data_frame2)

    data3 = {
        "id": [300, 400],
        "table2_id": [1, 1]
    }
    data_frame3 = pd.DataFrame(data3)
    table3 = Table3(data_frame=data_frame3)

    with pytest.raises(cubista.CannotEvaluateFields):
        _ = cubista.DataSource(tables=[
            table3,
            table2,
            table1,
        ])

def test_when_field_is_calculated_it_is_evaluated():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()
            name_length = cubista.CalculatedField(lambda x: len(x["name"]), source_fields=["name"])

    data1 = {
        "id": [1, 2, 3],
        "name": ["one", "two", "three"]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    _ = cubista.DataSource(tables=[
        table1
    ])

    assert table1.data_frame["name_length"].tolist() == [3, 3, 5]

def test_when_field_is_calculated_only_source_fields_are_sent_to_lambda():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()
            email = cubista.StringField()
            only_source_fields_sent_to_lambda = cubista.CalculatedField(lambda x: x.index.tolist() == ["name", "email"], source_fields=["name", "email"])

    data1 = {
        "id": [1],
        "name": ["one"],
        "email": ["a@b.com"]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    _ = cubista.DataSource(tables=[
        table1
    ])

    assert table1.data_frame["only_source_fields_sent_to_lambda"].tolist() == [True]

def test_create_table_with_grouping_aggregation_and_filtering():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            name = cubista.StringField()
            value = cubista.FloatField()

    class Table2(cubista.AggregatedTable):
        class Aggregation:
            source: cubista.Table = lambda: Table1
            sort_by = ["id"]
            group_by = ["name"]
            filter = lambda x: x["name"] != "group 3"
            filter_fields = ["name"]

        class Fields:
            id = cubista.AggregatedTableAutoIncrementPrimaryKeyField()
            table1_name = cubista.AggregatedTableGroupField(source="name")
            table1_value_sum = cubista.AggregatedTableAggregateField(source="value", aggregate_function="sum")

    data1 = {
        "id": [1, 2, 3, 4, 5, 6],
        "name": ["group 1", "group 1", "group 2", "group 2", "group 3", "group 3"],
        "value": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    table2 = Table2()

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    assert table2.data_frame.columns.tolist() == ["table1_name", "table1_value_sum", "id"]
    assert table2.data_frame["id"].tolist() == [-2, -3]
    assert table2.data_frame["table1_name"].tolist() == ["group 1", "group 2"]
    assert table2.data_frame["table1_value_sum"].tolist() == [3.0, 7.0]

def test_create_aggregated_foreign_field_migrates_to_table():
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

def test_calculate_cum_sum_field():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            task_id = cubista.IntField()
            date = cubista.DateField()
            time_spent = cubista.FloatField()
            time_spent_cumsum = cubista.CumSumField(source_field="time_spent", group_by=["task_id"], sort_by=["date"])


    data1 = {
        "id": [1, 2, 3, 4, 5, 6],
        "task_id": [10, 20, 10, 20, 10, 20],
        "date": [
            datetime.date(year=2021, month=9, day=4),
            datetime.date(year=2021, month=9, day=4),
            datetime.date(year=2021, month=9, day=5),
            datetime.date(year=2021, month=9, day=5),
            datetime.date(year=2021, month=9, day=6),
            datetime.date(year=2021, month=9, day=6),
        ],
        "time_spent": [
            1.0, 2.0, 3.0, 4.0, 5.0, 6.0
        ]
    }

    data_frame1 = pd.DataFrame(data1)

    table1 = Table1(data_frame=data_frame1)

    _ = cubista.DataSource(tables=[
        table1,
    ])

    assert table1.data_frame["time_spent_cumsum"].tolist() == [1.0, 2.0, 4.0, 6.0, 9.0, 12.0]
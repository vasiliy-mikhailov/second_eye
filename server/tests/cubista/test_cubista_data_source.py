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

def test_when_aggregated_table_created_with_non_autoincrement_primary_key_then_primary_key_values_are_valid():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            category_id = cubista.IntField()
            value = cubista.FloatField()

    class Table2(cubista.AggregatedTable):
        class Aggregation:
            source: cubista.Table = lambda: Table1
            sort_by = ["id"]
            group_by = ["category_id"]
            filter = None
            filter_fields = []

        class Fields:
            id = cubista.AggregatedTableGroupField(source="category_id", primary_key=True)
            value_sum = cubista.AggregatedTableAggregateField(source="value", aggregate_function="sum")

    data1 = {
        "id": [1, 2, 3, 4, 5, 6],
        "category_id": [1, 1, 2, 2, 3, 3],
        "value": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    table2 = Table2()

    _ = cubista.DataSource(tables=[
        table1,
        table2
    ])

    assert table2.data_frame.columns.tolist() == ["id", "value_sum"]
    assert table2.data_frame["id"].tolist() == [1, 2, 3]
    assert table2.data_frame["value_sum"].tolist() == [3.0, 7.0, 11.0]

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

def test_create_table_with_outer_join():
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

    _ = cubista.DataSource(tables=[
        table1,
        table2,
        table3
    ])

    assert sorted(table3.data_frame.columns.tolist()) == sorted(["id", "key1", "key2", "plan_value", "fact_value"])
    assert table3.data_frame["id"].tolist() == [-2, -3, -4]
    assert table3.data_frame["key1"].tolist() == [10, 10, 10]
    assert table3.data_frame["key2"].tolist() == [20, 30, 40]
    assert table3.data_frame["plan_value"].tolist() == [1.0, 2.0, 0.0]
    assert table3.data_frame["fact_value"].tolist() == [3.0, 0.0, 4.0]

def test_create_cross_table_with_outer_join():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)

    class Table3(cubista.OuterJoinedTable):
        class OuterJoin:
            left_source_table: cubista.Table = lambda: Table1
            right_source_table: cubista.Table = lambda: Table2
            left_fields = {"id": "id_1"}
            right_fields = {"id": "id_2"}
            on_fields = []

        class Fields:
            id = cubista.OuterJoinedTableTableAutoIncrementPrimaryKeyField()
            id_1 = cubista.OuterJoinedTableOuterJoinedField(source="id_1", default=-1)
            id_2 = cubista.OuterJoinedTableOuterJoinedField(source="id_2", default=-1)

    data1 = {
        "id": [1, 2],
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [3, 4],
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    table3 = Table3()

    _ = cubista.DataSource(tables=[
        table1,
        table2,
        table3
    ])

    assert sorted(table3.data_frame.columns.tolist()) == sorted(["id", "id_1", "id_2"])
    assert table3.data_frame["id"].tolist() == [-2, -3, -4, -5]
    assert table3.data_frame["id_1"].tolist() == [1, 1, 2, 2]
    assert table3.data_frame["id_2"].tolist() == [3, 4, 3, 4]

def test_create_union_table():
    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key1 = cubista.IntField(nulls=True, unique=False)
            key2 = cubista.IntField(nulls=True, unique=False)
            value = cubista.FloatField()

    class Table2(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            key1 = cubista.IntField(nulls=True, unique=False)
            key2 = cubista.IntField(nulls=True, unique=False)
            value = cubista.FloatField()

    class Table3(cubista.UnionTable):
        class Union:
            tables: [cubista.Table] = [lambda: Table1, lambda: Table2]
            fields: [str] = ["key1", "value"]

        class Fields:
            id = cubista.UnionTableTableAutoIncrementPrimaryKeyField()
            key1 = cubista.UnionTableUnionField(source="key1")
            value = cubista.UnionTableUnionField(source="value")

    data1 = {
        "id": [1, 2],
        "key1": [10, 10],
        "key2": [20, 30],
        "value": [1.0, 2.0]
    }
    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    data2 = {
        "id": [3, 4],
        "key1": [10, 10],
        "key2": [20, 40],
        "value": [3.0, 4.0]
    }
    data_frame2 = pd.DataFrame(data2)
    table2 = Table2(data_frame=data_frame2)

    table3 = Table3()

    _ = cubista.DataSource(tables=[
        table1,
        table2,
        table3
    ])

    assert sorted(table3.data_frame.columns.tolist()) == sorted(["id", "key1", "value"])
    assert table3.data_frame["id"].tolist() == [-2, -3, -4, -5]
    assert table3.data_frame["key1"].tolist() == [10, 10, 10, 10]
    assert table3.data_frame["value"].tolist() == [1.0, 2.0, 3.0, 4.0]

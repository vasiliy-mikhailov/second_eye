import pytest
import cubista
import pandas as pd

def test_field_pack_calculates_data():
    class SquaredNumber(cubista.FieldPack):
        class Fields:
            squared_number = cubista.CalculatedField(
                lambda_expression=lambda x: x["number"] ** 2,
                source_fields=["number"]
            )

    class Table1(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True)
            number = cubista.FloatField()

        class FieldPacks:
            field_packs = [lambda: SquaredNumber()]

    data1 = {
        "id": [1, 2],
        "number": [1, 2],
    }

    data_frame1 = pd.DataFrame(data1)
    table1 = Table1(data_frame=data_frame1)

    _ = cubista.DataSource(tables=[
        table1,
    ])

    assert sorted(table1.data_frame.columns.tolist()) == sorted(["id", "number", "squared_number"])
    assert table1.data_frame["id"].tolist() == [1, 2]
    assert table1.data_frame["number"].tolist() == [1.0, 2.0]
    assert table1.data_frame["squared_number"].tolist() == [1.0, 4.0]

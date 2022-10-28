import cubista
from second_eye_api.migrate_from_external_db.transform import time_sheet_by_date_model
import datetime
import pandas as pd

def test_when_time_sheet_by_date_model_gets_time_sheet_by_date_data_it_calculates_m_and_b():
    class TimeSheetByDateTable(cubista.Table):
        class Fields:
            id = cubista.IntField(primary_key=True, unique=True, nulls=False)
            planning_period_id = cubista.IntField()
            date = cubista.DateField()
            time_spent_cumsum = cubista.FloatField()

    class PlanningPeriodTimeSheetsByDateModelTable(time_sheet_by_date_model.ModelTable):
        class Model:
            source = lambda: TimeSheetByDateTable
            entity_id_field_name = "planning_period_id"

        class Fields:
            planning_period_id = time_sheet_by_date_model.EntityIdField(source="planning_period_id")
            time_sheets_by_date_model_m = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_m")
            time_sheets_by_date_model_b = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_b")
            time_sheets_by_date_model_min_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_min_date")
            time_sheets_by_date_model_max_date = time_sheet_by_date_model.ModelOutputField("time_sheets_by_date_model_max_date")

    planning_period_time_sheet_by_date_table = {
        "id": [1, 2, 3, 4],
        "planning_period_id": [1, 1, 2, 2],
        "date": [datetime.date(year=2021, month=1, day=1), datetime.date(year=2021, month=1, day=2), datetime.date(year=2021, month=1, day=1), datetime.date(year=2021, month=1, day=2)],
        "time_spent_cumsum": [1.0, 2.0, 2.0, 6.0]
    }
    planning_period_time_sheet_by_date_data_frame = pd.DataFrame(planning_period_time_sheet_by_date_table)
    planning_period_time_sheet_by_date_table = TimeSheetByDateTable(data_frame=planning_period_time_sheet_by_date_data_frame)

    planning_period_time_sheet_by_date_model_table = PlanningPeriodTimeSheetsByDateModelTable()

    _ = cubista.DataSource(tables=[
        planning_period_time_sheet_by_date_table,
        planning_period_time_sheet_by_date_model_table,
    ])

    assert planning_period_time_sheet_by_date_model_table.data_frame["planning_period_id"].tolist() == [1, 2]
    assert all([round(a, 2) == round(b, 2) for a, b in zip(planning_period_time_sheet_by_date_model_table.data_frame["time_sheets_by_date_model_m"], [1.0, 4.0])])
    assert all([round(a, 2) == round(b, 2) for a, b in zip(planning_period_time_sheet_by_date_model_table.data_frame["time_sheets_by_date_model_b"], [1.0, 2.0])])
    assert all([a == b for a, b in zip(planning_period_time_sheet_by_date_model_table.data_frame["time_sheets_by_date_model_min_date"], [datetime.date(year=2021, month=1, day=1), datetime.date(year=2021, month=1, day=1)])])
    assert all([a == b for a, b in zip(planning_period_time_sheet_by_date_model_table.data_frame["time_sheets_by_date_model_max_date"], [datetime.date(year=2021, month=1, day=2), datetime.date(year=2021, month=1, day=2)])])

import pandas as pd
import datetime

class TaskTimeSheetsExtractor:
    def extract(self):
        none_task_time_sheets = pd.DataFrame({
            "id": pd.Series(dtype=int),
            "task_id": pd.Series(dtype=str),
            "date": pd.Series(dtype=object),
            "time_spent": pd.Series(dtype=float),
            "person_id": pd.Series(dtype=str),
        })

        self.data = none_task_time_sheets

import pandas as pd
import datetime

class TaskTimeSheetsCreator:
    def __init__(self):
        self.last_id = 15
        self.task_time_sheets = [{
            "id": -1,
            "task_id": -1,
            "date": datetime.date.today(),
            "time_spent": 0,
            "person_key": "-1",
        }]

    def create_task_time_sheet(self, task_id, date, time_spent, person_key):
        id = self.last_id + 100
        task_time_sheets = self.task_time_sheets
        task_time_sheets.append(
            {
                "id": id,
                "task_id": task_id,
                "date": date,
                "time_spent": time_spent,
                "person_key": person_key,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        task_time_sheets = self.task_time_sheets
        self.data = pd.DataFrame(task_time_sheets)

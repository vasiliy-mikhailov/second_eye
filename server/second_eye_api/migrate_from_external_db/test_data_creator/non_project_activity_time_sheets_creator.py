import pandas as pd
import datetime

class NonProjectActivityTimeSheetsCreator:
    def __init__(self):
        self.last_id = 17
        self.non_project_activity_time_sheets = [{
            "id": -1,
            "non_project_activity_id": -1,
            "date": datetime.date.today(),
            "time_spent": 0,
            "person_key": "-1",
        }]

    def create_non_project_activity_time_sheet(self, non_project_activity_id, date, time_spent, person_key):
        id = self.last_id + 100
        non_project_activity_time_sheets = self.non_project_activity_time_sheets
        non_project_activity_time_sheets.append(
            {
                "id": id,
                "non_project_activity_id": non_project_activity_id,
                "date": date,
                "time_spent": time_spent,
                "person_key": person_key,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        non_project_activity_time_sheets = self.non_project_activity_time_sheets
        self.data = pd.DataFrame(non_project_activity_time_sheets)

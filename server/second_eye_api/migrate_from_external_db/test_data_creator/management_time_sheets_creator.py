import datetime
import pandas as pd

class ManagementTimeSheetsCreator:
    def __init__(self):
        self.last_id = 9
        self.management_time_sheets = [{
            "id": -1,
            "system_change_request_id": -1,
            "date": datetime.date.today(),
            "time_spent": 0,
            "person_key": "-1",
        }]

    def create_management_time_sheet(self, system_change_request_id, date, time_spent, person_key):
        id = self.last_id + 100
        management_time_sheets = self.management_time_sheets
        management_time_sheets.append(
            {
                "id": id,
                "system_change_request_id": system_change_request_id,
                "date": date,
                "time_spent": time_spent,
                "person_key": person_key,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        management_time_sheets = self.management_time_sheets
        self.data = pd.DataFrame(management_time_sheets)
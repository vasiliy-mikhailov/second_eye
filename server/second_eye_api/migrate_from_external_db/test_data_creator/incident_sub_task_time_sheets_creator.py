import pandas as pd
import datetime

class IncidentSubTaskTimeSheetsCreator:
    def __init__(self):
        self.last_id = 5
        self.incident_sub_task_time_sheets = [{
            "id": -1,
            "incident_sub_task_id": -1,
            "date": datetime.date.today(),
            "time_spent": 0,
            "person_key": "-1",
        }]

    def create_incident_sub_task_time_sheet(self, incident_sub_task_id, date, time_spent, person_key):
        id = self.last_id + 100
        incident_sub_task_time_sheets = self.incident_sub_task_time_sheets
        incident_sub_task_time_sheets.append(
            {
                "id": id,
                "incident_sub_task_id": incident_sub_task_id,
                "date": date,
                "time_spent": time_spent,
                "person_key": person_key,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        incident_sub_task_time_sheets = self.incident_sub_task_time_sheets
        self.data = pd.DataFrame(incident_sub_task_time_sheets)

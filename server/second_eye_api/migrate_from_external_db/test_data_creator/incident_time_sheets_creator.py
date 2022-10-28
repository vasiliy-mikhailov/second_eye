import pandas as pd
import datetime

class IncidentTimeSheetsCreator:
    def __init__(self):
        self.last_id = 7
        self.incident_time_sheets = [{
            "id": -1,
            "incident_id": -1,
            "date": datetime.date.today(),
            "time_spent": 0,
            "person_key": "-1",
        }]

    def create_incident_time_sheet(self, incident_id, date, time_spent, person_key):
        id = self.last_id + 100
        incident_time_sheets = self.incident_time_sheets
        incident_time_sheets.append(
            {
                "id": id,
                "incident_id": incident_id,
                "date": date,
                "time_spent": time_spent,
                "person_key": person_key,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        incident_time_sheets = self.incident_time_sheets
        self.data = pd.DataFrame(incident_time_sheets)

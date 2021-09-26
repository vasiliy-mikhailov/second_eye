import pandas as pd

class SystemChangeRequestsTimeSheetsExtractor:
    def extract(self):
        none_system_change_requests_time_sheets = pd.DataFrame([], columns=[
            "id",
            "system_change_request_id",
            "date",
            "time_spent",
            "person_id"
        ])

        self.data = none_system_change_requests_time_sheets
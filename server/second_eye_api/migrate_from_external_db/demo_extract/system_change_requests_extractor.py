import pandas as pd

class SystemChangeRequestsExtractor:
    def extract(self):
        system_change_request_not_specified = pd.DataFrame([[
            "-1",
            "",
            "Не указано",
            -1,
            0,
            0,
            0,
            0,
            0,
            0,
            "-1",
            "-1",
        ]], columns=[
            "id",
            "url",
            "name",
            "system_id",
            "analysis_preliminary_estimate",
            "development_preliminary_estimate",
            "testing_preliminary_estimate",
            "analysis_planned_estimate",
            "development_planned_estimate",
            "testing_planned_estimate",
            "change_request_id",
            "state_id",
        ])

        self.data = system_change_request_not_specified
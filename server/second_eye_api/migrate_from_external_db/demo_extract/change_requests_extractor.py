import pandas as pd

class ChangeRequestsExtractor:
    def extract(self):
        change_request_not_specified = pd.DataFrame([[
            "-1",
            "",
            "Не указано",
            0,
            0,
            0,
            0,
            "-1",
            None,
            -1,
            -1,
            0,
            None,
            None
        ]], columns=[
            "id",
            "url",
            "name",
            "express_estimate",
            "analysis_express_estimate",
            "development_express_estimate",
            "testing_express_estimate",
            "state_id",
            "planned_install_date",
            "year_label_max",
            "project_team_id",
            "has_value",
            "resolution_date",
            "install_date"
        ])
        source_fields = ["install_date", "resolution_date", "planned_install_date", "year_label_max"]

        self.data = change_request_not_specified
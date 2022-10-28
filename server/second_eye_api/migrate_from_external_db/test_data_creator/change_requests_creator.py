import pandas as pd

class ChangeRequestsCreator:
    def __init__(self):
        self.last_id = 0
        self.change_requests = [{
            "id": -1,
            "key": "-1",
            "url": "",
            "name": "Не указано",
            "analysis_express_estimate": 0,
            "development_express_estimate": 0,
            "testing_express_estimate": 0,
            "state_id": "-1",
            "planned_install_date": None,
            "year_label_max": -1,
            "project_team_id": -1,
            "has_value": 0,
            "is_reengineering": 0,
            "epic_id": -1,
            "quarter_key": "-1",
            "install_date": None,
            "resolution_date": None,
        }]

    def create_change_request(
            self, key, name, url="", analysis_express_estimate=0, development_express_estimate=0, testing_express_estimate=0,
            state_id="-1", planned_install_date=None, year_label_max=-1, project_team_id=-1, has_value=0, is_reengineering=0, epic_id=-1, quarter_key="-1",
            install_date=None, resolution_date=None
    ):
        id = self.last_id + 100
        change_requests = self.change_requests
        change_requests.append(
            {
                "id": id,
                "key": key,
                "url": url,
                "name": name,
                "analysis_express_estimate": analysis_express_estimate,
                "development_express_estimate": development_express_estimate,
                "testing_express_estimate": testing_express_estimate,
                "state_id": state_id,
                "planned_install_date": planned_install_date,
                "year_label_max": year_label_max,
                "project_team_id": project_team_id,
                "has_value": has_value,
                "is_reengineering": is_reengineering,
                "epic_id": epic_id,
                "quarter_key": quarter_key,
                "install_date": install_date,
                "resolution_date": resolution_date
             }
        )

        self.last_id = id
        return id


    def extract(self):
        change_requests = self.change_requests
        self.data = pd.DataFrame(change_requests)
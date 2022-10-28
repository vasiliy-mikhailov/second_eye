import pandas as pd

class SystemChangeRequestsCreator:
    def __init__(self):
        self.last_id = 13
        self.system_change_requests = [{
            "id": -1,
            "key": "-1",
            "url": "",
            "name": "Не указано",
            "system_id": -1,
            "analysis_preliminary_estimate": 0,
            "development_preliminary_estimate": 0,
            "testing_preliminary_estimate": 0,
            "analysis_planned_estimate": 0,
            "development_planned_estimate": 0,
            "testing_planned_estimate": 0,
            "change_request_id": -1,
            "state_id": "-1",
        }]

    def create_system_change_request(self, key, name, change_request_id, system_id=-1,
         analysis_preliminary_estimate=0, development_preliminary_estimate=0, testing_preliminary_estimate=0,
         analysis_planned_estimate=0, development_planned_estimate=0, testing_planned_estimate=0,
         state_id="-1"
     ):
        id = self.last_id + 100
        system_change_requests = self.system_change_requests
        system_change_requests.append(
            {
                "id": id,
                "key": key,
                "url": "",
                "name": name,
                "system_id": system_id,
                "analysis_preliminary_estimate": analysis_preliminary_estimate,
                "development_preliminary_estimate": development_preliminary_estimate,
                "testing_preliminary_estimate": testing_preliminary_estimate,
                "analysis_planned_estimate": analysis_planned_estimate,
                "development_planned_estimate": development_planned_estimate,
                "testing_planned_estimate": testing_planned_estimate,
                "change_request_id": change_request_id,
                "state_id": state_id,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        system_change_requests = self.system_change_requests
        self.data = pd.DataFrame(system_change_requests)
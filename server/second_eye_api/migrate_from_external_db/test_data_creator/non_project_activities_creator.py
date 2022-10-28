import pandas as pd

class NonProjectActivitiesCreator:
    def __init__(self):
        self.last_id = 10
        self.non_project_activities = [{
            "id": -1,
            "key": "-1",
            "name": "Не указано",
            "url": "",
            "company_id": -1,
        }]


    def create_non_project_activity(self, key, name="", url="", company_id=-1):
        id = self.last_id + 100
        non_project_activities = self.non_project_activities
        non_project_activities.append(
            {
                "id": id,
                "key": key,
                "name": name,
                "url": url,
                "company_id": company_id,
            }
        )

        self.last_id = id
        return id

    def extract(self):
        non_project_activities = self.non_project_activities
        self.data = pd.DataFrame(non_project_activities)
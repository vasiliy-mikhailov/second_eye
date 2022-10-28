import pandas as pd

class IncidentsSubTasksCreator:
    def __init__(self):
        self.last_id = 6
        self.incident_sub_tasks = [{
            "id": -1,
            "key": "-1",
            "url": "",
            "name": "Не указано",
            "skill_id": "-1",
            "time_left": 0,
            "time_original_estimate": 0,
            "incident_id": -1,
            "state_id": "-1",
        }]

    def create_incident_sub_task(self, key, name, incident_id, skill_id, url="", time_left=0, time_original_estimate=0, state_id="-1"):
        id = self.last_id + 100
        incident_sub_tasks = self.incident_sub_tasks
        incident_sub_tasks.append(
            {
                "id": id,
                "key": key,
                "url": url,
                "name": name,
                "skill_id": skill_id,
                "time_left": time_left,
                "time_original_estimate": time_original_estimate,
                "incident_id": incident_id,
                "state_id": state_id,
            }
        )

        self.last_id = id
        return id

    def extract(self):
        incident_sub_tasks = self.incident_sub_tasks
        self.data = pd.DataFrame(incident_sub_tasks)

import pandas as pd

class TasksCreator:
    def __init__(self):
        self.last_id = 16
        self.tasks = [{
            "id": -1,
            "key": "-1",
            "url": "",
            "name": "Не указано",
            "skill_id": -1,
            "time_left": 0,
            "time_original_estimate": 0,
            "system_change_request_id": -1,
            "state_id": "-1",
        }]


    def create_task(self, key, name, system_change_request_id, skill_id, url="", time_left=0, time_original_estimate=0, state_id="-1"):
        id = self.last_id + 100
        tasks = self.tasks
        tasks.append(
            {
                "id": id,
                "key": key,
                "url": url,
                "name": name,
                "skill_id": skill_id,
                "time_left": time_left,
                "time_original_estimate": time_original_estimate,
                "system_change_request_id": system_change_request_id,
                "state_id": state_id,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        tasks = self.tasks
        self.data = pd.DataFrame(tasks)

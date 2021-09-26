import pandas as pd

class TasksExtractor:
    def extract(self):
        task_not_specified = pd.DataFrame([[
            "-1",
            "",
            "Не указано",
            -1,
            0,
            0,
            "-1",
            "-1",
        ]], columns=[
            "id",
            "url",
            "name",
            "skill_id",
            "preliminary_estimate",
            "planned_estimate",
            "system_change_request_id",
            "state_id"
        ])

        self.data = task_not_specified

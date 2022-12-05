import pandas as pd

class FunctionComponentsCreator:
    def __init__(self):
        self.last_id = 17

        self.function_components = [{
            "id": -1,
            "key": "-1",
            "url": "",
            "name": "Не указано",
            "state_id": "-1",
            "task_id": -1,
            "kind_id": -1,
            "count": 0,
        }]

    def create_function_component(self, task_id, kind_id, name, count):
        id = self.last_id + 100
        function_components = self.function_components
        function_components.append(
            {
                "id": id,
                "key": str(id),
                "url": "",
                "name": name,
                "state_id": "-1",
                "task_id": task_id,
                "kind_id": kind_id,
                "count": count,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        function_components = self.function_components
        self.data = pd.DataFrame(function_components)
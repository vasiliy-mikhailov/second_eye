import pandas as pd

class FunctionComponentsCreator:
    def extract(self):
        none_none_function_components = pd.DataFrame([], columns=[
            "id",
            "key",
            "url",
            "name",
            "state_id",
            "task_id",
            "kind_id",
            "count"
        ])

        self.data = none_none_function_components
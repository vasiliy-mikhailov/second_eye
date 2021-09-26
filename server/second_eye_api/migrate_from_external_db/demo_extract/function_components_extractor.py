import pandas as pd

class FunctionComponentsExtractor:
    def extract(self):
        none_none_function_components = pd.DataFrame([], columns=[
            "id",
            "url",
            "name",
            "state_id",
            "task_id",
            "kind_id",
            "count"
        ])

        self.data = none_none_function_components
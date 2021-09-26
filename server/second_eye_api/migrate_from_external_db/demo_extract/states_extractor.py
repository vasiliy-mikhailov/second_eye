import pandas as pd

class StatesExtractor:
    def extract(self):
        state_not_specified = pd.DataFrame([[
            "-1",
            "Не указано",
        ]], columns=[
            "id",
            "name",
        ])

        self.data = state_not_specified
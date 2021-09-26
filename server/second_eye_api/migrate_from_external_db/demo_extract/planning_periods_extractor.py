import pandas as pd

class PlaningPeriodsExtractor:
    def extract(self):
        planning_period_not_specified = pd.DataFrame([
                [-1],
                [2021],
                [2022]
            ], columns=[
                "id"
            ]
        )

        self.data = planning_period_not_specified

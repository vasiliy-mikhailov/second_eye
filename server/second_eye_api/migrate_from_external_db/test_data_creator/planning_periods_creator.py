import pandas as pd

class PlaningPeriodsCreator:
    def __init__(self):
        self.planning_periods = [{
            "id": -1,
        }]

    def create_planning_period(self, id):
        planning_periods = self.planning_periods
        planning_periods.append(
            {
                "id": id,
             }
        )

    def extract(self):
        planning_periods = self.planning_periods
        self.data = pd.DataFrame(planning_periods)
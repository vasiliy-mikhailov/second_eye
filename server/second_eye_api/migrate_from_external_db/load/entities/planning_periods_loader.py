from second_eye_api.models.entities import PlanningPeriod
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class PlanningPeriodsLoader:
    def __init__(self, planning_periods, output_database):
        self.planning_periods = planning_periods
        self.output_database = output_database

    def load(self):
        planning_periods = self.planning_periods
        output_database = self.output_database

        load_dataframe_to_db(dataframe=planning_periods, model=PlanningPeriod, output_database=output_database)
from second_eye_api.models.entities import PlanningPeriodTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class PlanningPeriodTimeSheetsByDateLoader:
    def __init__(self, planning_period_time_sheets_by_date, output_database):
        self.planning_period_time_sheets_by_date = planning_period_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        planning_period_time_sheets_by_date = self.planning_period_time_sheets_by_date
        output_database = self.output_database

        load_dataframe_to_db(dataframe=planning_period_time_sheets_by_date, model=PlanningPeriodTimeSheetsByDate, output_database=output_database)
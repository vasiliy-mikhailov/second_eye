from second_eye_api.models.entities import DedicatedTeamPlanningPeriodTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class DedicatedTeamPlanningPeriodTimeSheetsByDateLoader:
    def __init__(self, dedicated_team_planning_period_time_sheets_by_date, output_database):
        self.dedicated_team_planning_period_time_sheets_by_date = dedicated_team_planning_period_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        dedicated_team_planning_period_time_sheets_by_date = self.dedicated_team_planning_period_time_sheets_by_date
        output_database = self.output_database

        load_dataframe_to_db(dataframe=dedicated_team_planning_period_time_sheets_by_date, model=DedicatedTeamPlanningPeriodTimeSheetsByDate, output_database=output_database)
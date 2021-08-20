from second_eye_api.models.entities import ProjectTeamPlanningPeriodTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ProjectTeamPlanningPeriodTimeSheetsByDateLoader:
    def __init__(self, project_team_planning_period_time_sheets_by_date, output_database):
        self.project_team_planning_period_time_sheets_by_date = project_team_planning_period_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        project_team_planning_period_time_sheets_by_date = self.project_team_planning_period_time_sheets_by_date
        output_database = self.output_database

        load_dataframe_to_db(dataframe=project_team_planning_period_time_sheets_by_date, model=ProjectTeamPlanningPeriodTimeSheetsByDate, output_database=output_database)
from second_eye_api.models import ProjectTeam
from second_eye_api.migrate_from_external_db.load.loader import load_dataframe_to_db

class ProjectTeamsLoader:
    def __init__(self, project_teams, output_database):
        self.project_teams = project_teams
        self.output_database = output_database

    def load(self):
        project_teams = self.project_teams
        output_database = self.output_database
        load_dataframe_to_db(dataframe=project_teams, model=ProjectTeam, output_database=output_database)

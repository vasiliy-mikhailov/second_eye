from second_eye_api.models.entities import ProjectTeamPosition
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ProjectTeamPositionsLoader:
    def __init__(self, project_team_positions, output_database):
        self.project_team_positions = project_team_positions
        self.output_database = output_database

    def load(self):
        project_team_positions = self.project_team_positions
        output_database = self.output_database
        load_dataframe_to_db(dataframe=project_team_positions, model=ProjectTeamPosition, output_database=output_database)
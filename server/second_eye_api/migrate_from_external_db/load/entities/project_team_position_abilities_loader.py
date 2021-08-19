from second_eye_api.models.entities import ProjectTeamPositionAbility
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ProjectTeamPositionAbilitiesLoader:
    def __init__(self, project_team_position_abilities, output_database):
        self.project_team_position_abilities = project_team_position_abilities
        self.output_database = output_database

    def load(self):
        project_team_position_abilities = self.project_team_position_abilities
        output_database = self.output_database
        load_dataframe_to_db(dataframe=project_team_position_abilities, model=ProjectTeamPositionAbility, output_database=output_database)
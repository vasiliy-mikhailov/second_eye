from second_eye_api.models.entities import DedicatedTeamPosition
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class DedicatedTeamPositionsLoader:
    def __init__(self, dedicated_team_positions, output_database):
        self.dedicated_team_positions = dedicated_team_positions
        self.output_database = output_database

    def load(self):
        dedicated_team_positions = self.dedicated_team_positions
        output_database = self.output_database
        load_dataframe_to_db(dataframe=dedicated_team_positions, model=DedicatedTeamPosition, output_database=output_database)

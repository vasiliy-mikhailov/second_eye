from second_eye_api.models import DedicatedTeamPositionAbility
from second_eye_api.migrate_from_external_db.load.loader import load_dataframe_to_db

class DedicatedTeamPositionAbilitiesLoader:
    def __init__(self, dedicated_team_position_abilities, output_database):
        self.dedicated_team_position_abilities = dedicated_team_position_abilities
        self.output_database = output_database

    def load(self):
        dedicated_team_position_abilities = self.dedicated_team_position_abilities
        output_database = self.output_database
        load_dataframe_to_db(dataframe=dedicated_team_position_abilities, model=DedicatedTeamPositionAbility, output_database=output_database)
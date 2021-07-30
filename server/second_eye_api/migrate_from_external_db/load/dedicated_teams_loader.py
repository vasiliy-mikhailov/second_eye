from second_eye_api.models import DedicatedTeam
from second_eye_api.migrate_from_external_db.load.load import load_dataframe_to_db

class LoadDedicatedTeams:
    def __init__(self, dedicated_teams, output_database):
        self.dedicated_teams = dedicated_teams
        self.output_database = output_database

    def load(self):
        dedicated_teams = self.dedicated_teams
        output_database = self.output_database
        load_dataframe_to_db(dataframe=dedicated_teams, model=DedicatedTeam, output_database=output_database)

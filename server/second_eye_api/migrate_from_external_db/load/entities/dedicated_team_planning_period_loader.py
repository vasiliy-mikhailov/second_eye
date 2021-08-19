from second_eye_api.models.entities import DedicatedTeamPlanningPeriod
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class DedicatedTeamPlanningPeriodsLoader:
    def __init__(self, dedicated_team_planning_periods, output_database):
        self.dedicated_team_planning_periods = dedicated_team_planning_periods
        self.output_database = output_database

    def load(self):
        dedicated_team_planning_periods = self.dedicated_team_planning_periods
        output_database = self.output_database

        load_dataframe_to_db(dataframe=dedicated_team_planning_periods, model=DedicatedTeamPlanningPeriod, output_database=output_database)
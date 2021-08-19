from second_eye_api.models.entities import ProjectTeamPlanningPeriod
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ProjectTeamPlanningPeriodsLoader:
    def __init__(self, project_team_planning_periods, output_database):
        self.project_team_planning_periods = project_team_planning_periods
        self.output_database = output_database

    def load(self):
        project_team_planning_periods = self.project_team_planning_periods
        output_database = self.output_database

        load_dataframe_to_db(dataframe=project_team_planning_periods, model=ProjectTeamPlanningPeriod, output_database=output_database)
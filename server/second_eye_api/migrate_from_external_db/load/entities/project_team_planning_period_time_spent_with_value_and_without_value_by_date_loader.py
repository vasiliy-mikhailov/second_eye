from second_eye_api.models.entities import ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader:
    def __init__(self, project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date, output_database):
        self.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date = project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date
        self.output_database = output_database

    def load(self):
        project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date = self.project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date
        output_database = self.output_database

        load_dataframe_to_db(dataframe=project_team_planning_period_time_spent_percent_with_value_and_without_value_by_date, model=ProjectTeamPlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate, output_database=output_database)
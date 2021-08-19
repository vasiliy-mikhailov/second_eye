from second_eye_api.models.entities import PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDateLoader:
    def __init__(self, planning_period_time_spent_percent_with_value_and_without_value_by_date, output_database):
        self.planning_period_time_spent_percent_with_value_and_without_value_by_date = planning_period_time_spent_percent_with_value_and_without_value_by_date
        self.output_database = output_database

    def load(self):
        planning_period_time_spent_percent_with_value_and_without_value_by_date = self.planning_period_time_spent_percent_with_value_and_without_value_by_date
        output_database = self.output_database

        load_dataframe_to_db(dataframe=planning_period_time_spent_percent_with_value_and_without_value_by_date, model=PlanningPeriodTimeSpentPercentWithValueAndWithoutValueByDate, output_database=output_database)
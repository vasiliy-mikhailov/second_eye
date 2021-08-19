from second_eye_api.models.entities import TaskTimeSheets
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class TaskTimeSheetsLoader:
    def __init__(self, task_time_sheets, output_database):
        self.task_time_sheets = task_time_sheets
        self.output_database = output_database

    def load(self):
        task_time_sheets = self.task_time_sheets
        output_database = self.output_database
        load_dataframe_to_db(dataframe=task_time_sheets, model=TaskTimeSheets, output_database=output_database)
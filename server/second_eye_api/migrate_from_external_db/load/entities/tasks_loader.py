from second_eye_api.models.entities import Task
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class TasksLoader:
    def __init__(self, tasks, output_database):
        self.tasks = tasks
        self.output_database = output_database

    def load(self):
        tasks = self.tasks
        output_database = self.output_database
        load_dataframe_to_db(dataframe=tasks, model=Task, output_database=output_database)
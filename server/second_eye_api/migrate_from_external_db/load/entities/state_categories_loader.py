from second_eye_api.models.entities import StateCategory
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class StateCategoriessLoader:
    def __init__(self, state_categories, output_database):
        self.state_categories = state_categories
        self.output_database = output_database

    def load(self):
        state_categories = self.state_categories
        output_database = self.output_database
        load_dataframe_to_db(dataframe=state_categories, model=StateCategory, output_database=output_database)
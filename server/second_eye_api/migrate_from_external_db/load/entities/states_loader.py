from second_eye_api.models.entities import State
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class StatesLoader:
    def __init__(self, states, output_database):
        self.states = states
        self.output_database = output_database

    def load(self):
        states = self.states
        output_database = self.output_database
        load_dataframe_to_db(dataframe=states, model=State, output_database=output_database)
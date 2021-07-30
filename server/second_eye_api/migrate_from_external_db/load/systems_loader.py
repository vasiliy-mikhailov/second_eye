from second_eye_api.models import System
from second_eye_api.migrate_from_external_db.load.loader import load_dataframe_to_db

class SystemsLoader:
    def __init__(self, systems, output_database):
        self.systems = systems
        self.output_database = output_database

    def load(self):
        systems = self.systems
        output_database = self.output_database
        load_dataframe_to_db(dataframe=systems, model=System, output_database=output_database)
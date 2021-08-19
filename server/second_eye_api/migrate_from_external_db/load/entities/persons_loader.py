from second_eye_api.models.entities import Person
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class PersonsLoader:
    def __init__(self, persons, output_database):
        self.persons = persons
        self.output_database = output_database

    def load(self):
        persons = self.persons
        output_database = self.output_database
        load_dataframe_to_db(dataframe=persons, model=Person, output_database=output_database)
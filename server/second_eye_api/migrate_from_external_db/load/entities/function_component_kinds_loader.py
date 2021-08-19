from second_eye_api.models.entities import FunctionComponentKind
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class FunctionComponentKindsLoader:
    def __init__(self, functionComponentKinds, output_database):
        self.functionComponentKinds = functionComponentKinds
        self.output_database = output_database

    def load(self):
        functionComponentKinds = self.functionComponentKinds
        output_database = self.output_database
        load_dataframe_to_db(dataframe=functionComponentKinds, model=FunctionComponentKind, output_database=output_database)

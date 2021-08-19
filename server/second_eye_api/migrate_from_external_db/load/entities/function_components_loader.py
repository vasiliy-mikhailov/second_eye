from second_eye_api.models.entities import FunctionComponent
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class FunctionComponentsLoader:
    def __init__(self, function_components, output_database):
        self.function_components = function_components
        self.output_database = output_database

    def load(self):
        function_components = self.function_components
        output_database = self.output_database
        load_dataframe_to_db(dataframe=function_components, model=FunctionComponent, output_database=output_database)
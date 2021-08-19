from second_eye_api.models.entities import SystemChangeRequest
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class SystemChangeRequestsLoader:
    def __init__(self, system_change_requests, output_database):
        self.system_change_requests = system_change_requests
        self.output_database = output_database

    def load(self):
        system_change_requests = self.system_change_requests
        output_database = self.output_database
        load_dataframe_to_db(dataframe=system_change_requests, model=SystemChangeRequest, output_database=output_database)
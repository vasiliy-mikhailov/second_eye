from second_eye_api.models import ChangeRequest
from second_eye_api.migrate_from_external_db.load.loader import load_dataframe_to_db

class ChangeRequestsLoader:
    def __init__(self, change_requests, output_database):
        self.change_requests = change_requests
        self.output_database = output_database

    def load(self):
        change_requests = self.change_requests
        output_database = self.output_database
        load_dataframe_to_db(dataframe=change_requests, model=ChangeRequest, output_database=output_database)
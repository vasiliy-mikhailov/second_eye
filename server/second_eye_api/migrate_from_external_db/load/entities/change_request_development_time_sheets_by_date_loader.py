from second_eye_api.models.entities import ChangeRequestDevelopmentTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ChangeRequestDevelopmentTimeSheetsByDateLoader:
    def __init__(self, change_request_development_time_sheets_by_date, output_database):
        self.change_request_development_time_sheets_by_date = change_request_development_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        change_request_development_time_sheets_by_date = self.change_request_development_time_sheets_by_date
        output_database = self.output_database
        load_dataframe_to_db(dataframe=change_request_development_time_sheets_by_date, model=ChangeRequestDevelopmentTimeSheetsByDate, output_database=output_database)
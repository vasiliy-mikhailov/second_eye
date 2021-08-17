from second_eye_api.models.entities import SystemChangeRequestTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class SystemChangeRequestTimeSheetsByDateLoader:
    def __init__(self, system_change_request_time_sheets_by_date, output_database):
        self.system_change_request_time_sheets_by_date = system_change_request_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        system_change_request_time_sheets_by_date = self.system_change_request_time_sheets_by_date
        output_database = self.output_database
        load_dataframe_to_db(dataframe=system_change_request_time_sheets_by_date, model=SystemChangeRequestTimeSheetsByDate, output_database=output_database)
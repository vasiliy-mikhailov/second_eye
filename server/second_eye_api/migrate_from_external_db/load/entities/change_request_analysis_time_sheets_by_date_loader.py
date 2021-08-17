from second_eye_api.models.entities import ChangeRequestAnalysisTimeSheetsByDate
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class ChangeRequestAnalysisTimeSheetsByDateLoader:
    def __init__(self, change_request_analysis_time_sheets_by_date, output_database):
        self.change_request_analysis_time_sheets_by_date = change_request_analysis_time_sheets_by_date
        self.output_database = output_database

    def load(self):
        change_request_analysis_time_sheets_by_date = self.change_request_analysis_time_sheets_by_date
        output_database = self.output_database
        load_dataframe_to_db(dataframe=change_request_analysis_time_sheets_by_date, model=ChangeRequestAnalysisTimeSheetsByDate, output_database=output_database)
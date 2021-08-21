from second_eye_api.models.entities import Company
from second_eye_api.migrate_from_external_db.load.utils import load_dataframe_to_db

class CompaniesLoader:
    def __init__(self, companies, output_database):
        self.companies = companies
        self.output_database = output_database

    def load(self):
        companies = self.companies
        output_database = self.output_database
        load_dataframe_to_db(dataframe=companies, model=Company, output_database=output_database)
from second_eye_api.models import Skill
from second_eye_api.migrate_from_external_db.load.loader import load_dataframe_to_db

class SkillsLoader:
    def __init__(self, skills, output_database):
        self.skills = skills
        self.output_database = output_database

    def load(self):
        skills = self.skills
        output_database = self.output_database
        load_dataframe_to_db(dataframe=skills, model=Skill, output_database=output_database)

import pandas as pd

class PersonsExtractor:
    def extract(self):
        person_not_specified = pd.DataFrame([["-1", "Не указано", False]], columns=["id", "name", "is_active"])

        self.data = person_not_specified
import pandas as pd

class CompaniesExtractor:
    def extract(self):
        companiesArray = [
            (-1, "Не указано"),
            (1, "МКБ"),
        ]

        self.data = pd.DataFrame.from_records(companiesArray, columns=["id", "name"])
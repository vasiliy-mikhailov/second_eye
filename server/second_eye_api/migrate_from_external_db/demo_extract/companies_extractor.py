import pandas as pd

class CompaniesExtractor:
    def extract(self):
        companiesArray = [
            [1, "Банк"],
            [2, "Брокер"],
            [3, "Телеком"],
        ]

        self.data = pd.DataFrame(companiesArray, columns=["id", "name"])
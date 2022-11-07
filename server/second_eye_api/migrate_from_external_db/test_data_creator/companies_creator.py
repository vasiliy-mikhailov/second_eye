import pandas as pd

class CompaniesCreator:
    def __init__(self):
        self.last_id = 2
        self.companies = [{
            "id": -1,
            "name": "Не указано",
        }]

    def create_company(self, name, id=None):
        if not id:
            id = self.last_id + 100

        companies = self.companies
        companies.append(
            {
                "id": id,
                "name": name,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        companies = self.companies
        self.data = pd.DataFrame(companies)
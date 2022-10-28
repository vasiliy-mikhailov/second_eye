import pandas as pd

class QuartersCreator:
    def __init__(self):
        self.quarters = [{
            "id": -1,
            "name": "Не указано",
            "year": -1,
            "quarter_number": -1,
        }]

    def create_quarter(self, name, year, quarter_number):
        id = year * 10 + quarter_number
        quarters = self.quarters
        quarters.append(
            {
                "id": id,
                "name": name,
                "year": year,
                "quarter_number": quarter_number,
             }
        )

        return id

    def extract(self):
        quarters = self.quarters
        self.data = pd.DataFrame(quarters)
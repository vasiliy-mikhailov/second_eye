import pandas as pd

class QuartersExtractor:
    def extract(self):
        quarters_array = [
            [ -1, "Не указано", -1, -1 ],
            [ 20221, "2022-I", 2022, 1 ],
            [ 20222, "2022-II", 2022, 2 ],
            [ 20223, "2022-III", 2022, 3 ],
            [ 20224, "2022-IV", 2022, 4 ],
        ]

        self.data = pd.DataFrame(quarters_array, columns=["id", "name", "year", "quarter_number"])
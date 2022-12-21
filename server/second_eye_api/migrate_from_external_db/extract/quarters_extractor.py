import pandas as pd

class QuartersExtractor:
    def extract(self):
        quarters_array = [
            [ -1, "Не указано", -1, -1 ],
            [ 20221, "2022-I", 2022, 1 ],
            [ 20222, "2022-II", 2022, 2 ],
            [ 20223, "2022-III", 2022, 3 ],
            [ 20224, "2022-IV", 2022, 4 ],
            [ 20231, "2023-I", 2023, 1],
            [ 20232, "2023-II", 2023, 2],
            [ 20233, "2023-III", 2023, 3],
            [ 20234, "2023-IV", 2023, 4],
        ]

        self.data = pd.DataFrame(quarters_array, columns=["id", "name", "year", "quarter_number"])
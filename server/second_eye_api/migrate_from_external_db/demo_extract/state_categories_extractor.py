import pandas as pd

class StateCategoriesExtractor:
    def extract(self):
        stateCategoriesArray = [
            (-1, 'Не указано'),
            (1, 'Сделать'),
            (2, 'В процессе'),
            (3, 'Сделано'),
            (4, 'Прочее')
        ]

        self.data = pd.DataFrame.from_records(stateCategoriesArray, columns=["id", "name"])
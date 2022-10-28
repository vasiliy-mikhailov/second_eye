import pandas as pd

class StateCategoriesCreator:
    def extract(self):
        state_categories = [
            (-1, 'Не указано'),
            (1, 'Сделать'),
            (2, 'В процессе'),
            (3, 'Сделано'),
            (4, 'Прочее')
        ]

        self.data = pd.DataFrame.from_records(state_categories, columns=["id", "name"])
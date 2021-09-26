import pandas as pd

class FunctionComponentKindsExtractor:
    def extract(self):
        functionComponentKindsArray = [
            (-1, 'Не указано', 0),
            (1, 'Вход', 4),
            (2, 'Выход', 5),
            (3, 'Таблица', 10),
            (4, 'Сообщение', 4),
            (5, 'Интерфейс', 7),
        ]

        self.data = pd.DataFrame.from_records(functionComponentKindsArray, columns=["id", "name", "function_points"])
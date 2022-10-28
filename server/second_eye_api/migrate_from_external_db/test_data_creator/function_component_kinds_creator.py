import pandas as pd

class FunctionComponentKindsCreator:
    def extract(self):
        function_component_kinds = [
            (-1, 'Не указано', 0),
            (1, 'Вход', 4),
            (2, 'Выход', 5),
            (3, 'Таблица', 10),
            (4, 'Сообщение', 4),
            (5, 'Интерфейс', 7),
        ]

        self.data = pd.DataFrame.from_records(function_component_kinds, columns=["id", "name", "function_points"])
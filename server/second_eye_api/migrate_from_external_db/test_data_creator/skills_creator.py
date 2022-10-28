import pandas as pd

class SkillsCreator:
    def extract(self):
        skills = [
            (-1, 'Не указано'),
            (1, 'Аналитика'),
            (2, 'Разработка'),
            (3, 'Тестирование'),
        ]

        self.data = pd.DataFrame.from_records(skills, columns=["id", "name"])
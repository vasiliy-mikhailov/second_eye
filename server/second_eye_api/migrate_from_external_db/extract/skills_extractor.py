import pandas as pd

class SkillsExtractor:
    def extract(self):
        skillsArray = [
            (-1, 'Не указано'),
            (1, 'Аналитика'),
            (2, 'Разработка'),
            (3, 'Тестирование'),
        ]

        self.data = pd.DataFrame.from_records(skillsArray, columns=["id", "name"])
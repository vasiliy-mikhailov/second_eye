import numpy as np
import pandas as pd

class SkillsExtractor:
    def extract(self):
        skillsArray = np.array([
            (1, 'Аналитика'),
            (2, 'Разработка'),
            (3, 'Тестирование')
        ])

        self.data = pd.DataFrame.from_records(skillsArray, columns=["id", "name"], index="id")
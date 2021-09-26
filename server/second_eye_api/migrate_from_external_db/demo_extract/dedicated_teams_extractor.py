import pandas as pd

class DedicatedTeamsExtractor:
    def extract(self):
        dedicated_team_not_specified = pd.DataFrame([
                [-1, "Не указано", 1],
                [1, "Корпоративный блок", 1],
                [2, "Розничный блок", 1],
                [3, "Инвестиционный блок", 1],
                [4, "Прайват банкинг", 1],
                [5, "Бекофис", 1],
            ], columns=["id", "name", "company_id"]
        )

        self.data = dedicated_team_not_specified

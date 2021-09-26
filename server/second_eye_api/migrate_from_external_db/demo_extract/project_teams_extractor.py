import pandas as pd

class ProjectTeamsExtractor:
    def extract(self):
        project_team_not_specified = pd.DataFrame([
                [-1, -1, "Не указано"],
                [1, 1, "Крупный бизнес"],
                [2, 1, "Средний бизнес"],
                [3, 1, "Малый и микробизнес"],
                [4, 1, "Привлечение, онбординг и процессы обслуживания корпоратов"],
                [5, 1, "Дистанционное банковское обслуживание"],
                [6, 1, "Факторинг"],
                [7, 1, "Корпоративное кредитование"],
                [8, 1, "Корпоративные депозиты"],
            ],columns=["id", "dedicated_team_id", "name"]
        )

        self.data = project_team_not_specified
import pandas as pd

class DedicatedTeamsCreator:
    def __init__(self):
        self.last_id = 3
        self.dedicated_teams = [{
            "id": -1,
            "name": "Не указано",
            "cio_key": "-1",
            "cto_key": "-1",
            "company_id": -1
        }]

    def create_dedicated_team(self, name, cio_key="-1", cto_key="-1", company_id=-1):
        id = self.last_id + 100
        dedicated_teams = self.dedicated_teams
        dedicated_teams.append(
            {
                "id": id,
                "name": name,
                "cio_key": cio_key,
                "cto_key": cto_key,
                "company_id": company_id,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        dedicated_teams = self.dedicated_teams
        self.data = pd.DataFrame(dedicated_teams)


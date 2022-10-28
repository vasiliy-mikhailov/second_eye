import pandas as pd

class ProjectTeamsCreator:
    def __init__(self):
        self.last_id = 12
        self.project_teams = [{
            "id": -1,
            "name": "Не указано",
            "url": "",
            "project_manager_key": "-1",
            "dedicated_team_id": -1,
        }]

    def create_project_team(self, name, url="", dedicated_team_id=-1, project_manager_key="-1"):
        id = self.last_id + 100
        project_teams = self.project_teams
        project_teams.append(
            {
                "id": id,
                "name": name,
                "url": url,
                "project_manager_key": project_manager_key,
                "dedicated_team_id": dedicated_team_id,
             }
        )

        self.last_id = id
        return id

    def extract(self):
        project_teams = self.project_teams
        self.data = pd.DataFrame(project_teams)

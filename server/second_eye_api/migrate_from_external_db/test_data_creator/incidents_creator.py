import pandas as pd

class IncidentsCreator:
    def __init__(self):
        self.last_id = 8
        self.incidents = [{
            "id": -1,
            "key": "-1",
            "name": "Не указано",
            "url": "",
            "system_id": -1,
            "state_id": -1,
            "install_date": None,
            "planned_install_date": None,
            "resolution_date": None,
            "year_label_max": -1,
            "project_team_id": -1,
        }]


    def create_incident(self, key, name="", url="", system_id=-1, state_id=-1, install_date=None, planned_install_date=None, resolution_date=None, year_label_max=-1, project_team_id=-1):
        id = self.last_id + 100
        incidents = self.incidents
        incidents.append(
            {
                "id": id,
                "key": key,
                "name": name,
                "url": url,
                "system_id": system_id,
                "state_id": state_id,
                "install_date": install_date,
                "planned_install_date": planned_install_date,
                "resolution_date": resolution_date,
                "year_label_max": year_label_max,
                "project_team_id": project_team_id,
            }
        )

        self.last_id = id
        return id

    def extract(self):
        incidents = self.incidents
        self.data = pd.DataFrame(incidents)
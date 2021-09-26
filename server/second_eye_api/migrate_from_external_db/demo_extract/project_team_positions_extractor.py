import pandas as pd

class ProjectTeamPositionsExtractor:
    def extract(self):
        none_project_team_position_abilities = pd.DataFrame([], columns=[
            "id",
            "url",
            "name",
            "incident_capacity",
            "management_capacity",
            "change_request_capacity",
            "other_capacity",
            "person_id",
            "project_team_id"
        ])

        self.data = none_project_team_position_abilities
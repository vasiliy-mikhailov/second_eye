import pandas as pd

class DedicatedTeamPositionsExtractor:
    def extract(self):
        none_dedicated_team_position_abilities = pd.DataFrame([], columns=[
            "id",
            "url",
            "name",
            "incident_capacity",
            "management_capacity",
            "change_request_capacity",
            "other_capacity",
            "person_id",
            "dedicated_team_id"
        ])

        self.data = none_dedicated_team_position_abilities
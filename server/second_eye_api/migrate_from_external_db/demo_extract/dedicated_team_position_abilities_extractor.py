import pandas as pd

class DedicatedTeamPositionAbilitiesExtractor:
    def extract(self):
        none_dedicated_team_position_abilities = pd.DataFrame(columns=[
            "id",
            "url",
            "name",
            "system_id",
            "dedicated_team_position_id",
            "skill_id"
        ])

        self.data = none_dedicated_team_position_abilities
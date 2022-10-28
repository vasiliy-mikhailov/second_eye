import pandas as pd

class ProjectTeamPositionAbilitiesCreator:
    def extract(self):
        none_project_team_position_abilities = pd.DataFrame([], columns=[
            "id",
            "url",
            "name",
            "system_id",
            "project_team_position_id",
            "skill_id"
        ])

        self.data = none_project_team_position_abilities
import pandas as pd

class ProjectTeamPositionsCreator:
    def extract(self):
        project_team_positions = pd.DataFrame([], columns=[
            "id",
            "url",
            "name",
            "incident_capacity",
            "management_capacity",
            "change_request_capacity",
            "other_capacity",
            "person_key",
            "project_team_id",
            "state_id"
        ])

        project_team_position_not_specified = pd.DataFrame([[
            -1,
            "",
            "Не указано",
            0,
            0,
            0,
            0,
            "-1",
            -1,
            "-1"
        ]], columns=[
            "id",
            "url",
            "name",
            "incident_capacity",
            "management_capacity",
            "change_request_capacity",
            "other_capacity",
            "person_key",
            "project_team_id",
            "state_id"
        ])
        project_team_positions = project_team_positions.append(
            project_team_position_not_specified,
            sort=False,
            ignore_index=True
        )

        self.data = project_team_positions
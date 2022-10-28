import pandas as pd

class DedicatedTeamPositionsCreator:
    def extract(self):
        dedicated_team_positions = pd.DataFrame([], columns=[
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

        dedicated_team_position_not_specified = pd.DataFrame([[
            -1,
            "",
            "Не указано",
            0,
            0,
            0,
            0,
            -1,
            -1
        ]], columns=[
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
        dedicated_team_positions = dedicated_team_positions.append(
            dedicated_team_position_not_specified,
            sort=False,
            ignore_index=True
        )

        self.data = dedicated_team_positions
import pandas as pd

class ProjectTeamsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select 
                    id as "id",
                    parentoptionid as "dedicated_team_id",
                    customvalue as "name"
                from 
                    jira60.customfieldoption
                where
                    customfield = 17127
                    and parentoptionid is not null
            """

            project_teams = pd.read_sql(query, connection)
            project_team_not_specified = pd.DataFrame(
                [[-1, -1, "Не указано"]],
                columns=["id", "dedicated_team_id", "name"]
            )
            project_teams = project_teams.append(
                project_team_not_specified,
                sort=False,
                ignore_index=True
            )

            self.data = project_teams
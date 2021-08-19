import pandas as pd

class DedicatedTeamsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select 
                    id as "id",
                    customvalue as "name"
                from 
                    jira60.customfieldoption
                where
                    customfield = 17127
                    and parentoptionid is null
            """

            data = pd.read_sql(query, connection)
            dedicated_team_not_specified = pd.DataFrame([[-1, "Не указано"]], columns=["id", "name"])
            data = data.append(
                dedicated_team_not_specified,
                sort=False)

            self.data = data

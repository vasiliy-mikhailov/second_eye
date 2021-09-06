import pandas as pd

class StatesExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select
                    id as "id",
                    pname as "name"
                from 
                    jira60.issuestatus
            """

            states = pd.read_sql(query, connection)

            state_not_specified = pd.DataFrame([[
                "-1",
                "Не указано",
            ]], columns=[
                "id",
                "name",
            ])

            states = states.append(
                state_not_specified
            )

            self.data = states
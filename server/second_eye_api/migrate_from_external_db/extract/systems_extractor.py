import pandas as pd

class SystemsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select
                    id as "id",
                    customValue as "name"
                from
                    jira60.customFieldOption system
                where
                    system.customField = 14713 -- Справочник систем
            """

            systems = pd.read_sql(query, connection)

            system_not_specified = pd.DataFrame(
                [[-1, "Не указано"]],
                columns=["id", "name"]
            )
            systems = systems.append(
                system_not_specified,
                sort=False,
                ignore_index=True
            )

            self.data = systems
import pandas as pd

class ExtractSystems:
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
                    jira60.customfieldoption system
                where
                    system.customfield = 15663 -- Справочник систем
            """

            systems = pd.read_sql(query, connection, index_col="id")

            system_not_specified = pd.DataFrame(
                [[-1, "Не указано"]],
                columns=["id", "name"]
            )
            systems = systems.reset_index().append(
                system_not_specified,
                sort=False).set_index(["id"])

            self.data = systems
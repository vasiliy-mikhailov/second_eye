import pandas as pd

class PersonsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                    lower(cwd_user.lower_user_name) as "id",
                    cwd_user.display_name as "name",
                    active "is_active"
                from
                    cwd_user
                order by
                    cwd_user.active desc, cwd_user.updated_date desc -- сначала активные и недавно обновленные (см. также drop_duplicates внизу)
            """

            persons = pd.read_sql(query, connection)
            persons = persons.drop_duplicates(subset=["id"]) # логины уволенных передаются новым

            person_not_specified = pd.DataFrame([[-1, "Не указано", False]], columns=["id", "name", "is_active"])
            persons = persons.reset_index().append(
                person_not_specified,
                sort=False).set_index(["id"]
            )

            self.data = persons
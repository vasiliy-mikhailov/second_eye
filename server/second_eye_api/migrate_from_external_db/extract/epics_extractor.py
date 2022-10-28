import pandas as pd

class EpicsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                    select
                        issue.id as "id",
                        project.pkey||'-'||issue.issuenum as "key",
                        'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                        issue.summary as "name",
                        1 as "company_id"
                    from
                        jira60.jiraissue issue
                        inner join jira60.project project on issue.project=project.id
                    where 
                        issue.issuetype=11007 --Epic
        """
            epics = pd.read_sql(
                query,
                connection
            )

            epic_not_specified = pd.DataFrame([[
                -1,
                "-1",
                "",
                "Не указано",
                -1
            ]], columns=[
                "id",
                "key",
                "url",
                "name",
                "company_id"
            ])
            epics = epics.append(
                epic_not_specified,
                ignore_index=True
            )

            self.data = epics
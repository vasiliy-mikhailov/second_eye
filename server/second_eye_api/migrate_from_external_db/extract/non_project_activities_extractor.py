import pandas as pd

class NonProjectActivitiesExtractor:
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
                    issue.issuetype = 12305 --текущая деятельность
                    and project.pkey = 'MKB'
        """

            non_project_activities = pd.read_sql(
                query,
                connection,
            )

            self.data = non_project_activities
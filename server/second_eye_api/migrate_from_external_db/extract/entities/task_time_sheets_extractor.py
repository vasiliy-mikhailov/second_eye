import pandas as pd

class TaskTimeSheetsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                    worklog.id as "id",
                    project.pkey||'-'||issue.issuenum as "task_id",
                    case when to_date('2017-01-01', 'YYYY-MM-DD') < trunc(worklog.startdate) then trunc(worklog.startdate) else to_date('2017-01-01', 'YYYY-MM-DD') end as "date",
                    worklog.timeworked / 60 / 60 as "time_spent",
                    lower(worklog.author) as "person_id"
                from
                    jira60.worklog
                    inner join jira60.jiraissue issue on (issue.id = worklog.issueid and issue.issuetype in (12904, 12703, 10603)) -- аналитика, разработка, тестирование
                    inner join jira60.project project on issue.project=project.id
                where
                    worklog.startdate <= sysdate
            """

            task_time_sheets = pd.read_sql(query, connection)

            self.data = task_time_sheets
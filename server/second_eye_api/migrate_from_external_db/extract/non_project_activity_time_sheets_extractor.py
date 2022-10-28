import pandas as pd

class NonProjectActivityTimeSheetsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                        worklog.id as "id",
                        issue.id as "non_project_activity_id",
                        case when to_date('2017-01-01', 'YYYY-MM-DD') < trunc(worklog.startdate) then trunc(worklog.startdate) else to_date('2017-01-01', 'YYYY-MM-DD') end as "date",
                        worklog.timeworked / 60 / 60 as "time_spent",
                        lower(worklog.author) as "person_key"
                    from
                        jira60.worklog
                        inner join jira60.jiraissue issue on (issue.id = worklog.issueid and issue.issuetype in (12305))
                    where
                        worklog.startdate <= sysdate
            """

            non_project_activity_time_sheets = pd.read_sql(query, connection, parse_dates={"date"})
            non_project_activity_time_sheets["date"] = non_project_activity_time_sheets["date"].dt.date

            self.data = non_project_activity_time_sheets
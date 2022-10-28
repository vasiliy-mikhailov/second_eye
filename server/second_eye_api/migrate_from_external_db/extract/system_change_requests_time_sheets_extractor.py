import pandas as pd

class SystemChangeRequestsTimeSheetsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                    worklog.id as "id",
                    issue.id as "system_change_request_id",
                    case when to_date('2017-01-01', 'YYYY-MM-DD') < trunc(worklog.startdate) then trunc(worklog.startdate) else to_date('2017-01-01', 'YYYY-MM-DD') end as "date",
                    worklog.timeworked / 60 / 60 as "time_spent",
                    lower(worklog.author) as "person_key"
                from
                    jira60.worklog
                    inner join jira60.jiraissue issue on (issue.id = worklog.issueid and issue.issuetype = 11901) -- доработка системы
                    inner join jira60.project project on issue.project=project.id
                where
                    worklog.startdate <= sysdate
            """

            system_change_request_time_sheets = pd.read_sql(query, connection, parse_dates={"date"})
            system_change_request_time_sheets["date"] = system_change_request_time_sheets["date"].dt.date

            self.data = system_change_request_time_sheets
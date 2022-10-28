import pandas as pd

class IncidentTimeSheetsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                        worklog.id as "id",
                        issue.id as "incident_id",
                        case when to_date('2017-01-01', 'YYYY-MM-DD') < trunc(worklog.startdate) then trunc(worklog.startdate) else to_date('2017-01-01', 'YYYY-MM-DD') end as "date",
                        worklog.timeworked / 60 / 60 as "time_spent",
                        lower(worklog.author) as "person_key"
                    from
                        jira60.worklog
                        inner join jira60.jiraissue issue on (issue.id = worklog.issueid and issue.issuetype in (10412))
                    where
                        worklog.startdate <= sysdate
            """

            incident_time_sheets = pd.read_sql(query, connection, parse_dates={"date"})
            incident_time_sheets["date"] = incident_time_sheets["date"].dt.date

            self.data = incident_time_sheets
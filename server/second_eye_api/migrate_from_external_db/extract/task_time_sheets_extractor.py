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
                    issue.id as "task_id",
                    case when to_date('2017-01-01', 'YYYY-MM-DD') < trunc(worklog.startdate) then trunc(worklog.startdate) else to_date('2017-01-01', 'YYYY-MM-DD') end as "date",
                    worklog.timeworked / 60 / 60 as "time_spent",
                    lower(worklog.author) as "person_key"
                from
                    jira60.worklog
                    inner join jira60.jiraissue issue on (issue.id = worklog.issueid and issue.issuetype in (12904, 12703, 10603, 12903)) -- аналитика, разработка, тестирование
                    inner join jira60.project project on issue.project=project.id
                    left join (
                        select
                            issue_link.*, (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank
                        from 
                            jira60.issuelink issue_link
                            inner join jira60.jiraissue system_change_request_issue on (
                                issue_link.source = system_change_request_issue.id
                                and issue_link.linktype in (11202, 11203, 11204, 11206) -- доработка системы <-> аналитика, разработка, тестирование, ошибка
                                and system_change_request_issue.issuetype = 11901 --доработка системы
                            )
                    ) issue_link on issue_link.destination = issue.id and issue_link.rank = 1 -- ограничить связь только с первой (по возрастанию id) доработкой системы
                    inner join jira60.jiraissue system_change_request_issue on issue_link.source = system_change_request_issue.id and issue_link.linktype in (11202, 11203, 11204, 11206) -- доработка системы <-> аналитика, разработка, тестирование
                where
                    worklog.startdate <= sysdate
                    and issue.issuetype in (12904, 12703, 10603, 12903) -- аналитика, разработка, тестирование, ошибка
            """

            task_time_sheets = pd.read_sql(query, connection, parse_dates={"date"})
            task_time_sheets["date"] = task_time_sheets["date"].dt.date

            self.data = task_time_sheets
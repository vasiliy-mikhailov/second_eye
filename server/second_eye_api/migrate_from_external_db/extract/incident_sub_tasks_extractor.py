import pandas as pd

class IncidentSubTasksExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                    issue.id as "id",
                    to_char(project.pkey||'-'||issue.issuenum) as "key",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                    issue.summary as "name",
                    CASE issue.issuetype
                        WHEN '12904' THEN 1
                        WHEN '12703' THEN 2
                        WHEN '10603' THEN 3
                    END as "skill_id",
                    nvl(issue.timeEstimate / 60 / 60, 0) as "time_left",
                    nvl(issue.timeOriginalEstimate / 60 / 60, 0) as "time_original_estimate",
                    incident_issue.id as "incident_id",
                    issue.issuestatus as "state_id"
                from 
                    jira60.jiraissue issue
                    inner join jira60.project project on issue.project=project.id
                    left join (
                        select
                            issue_link.*, (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank
                        from 
                            jira60.issuelink issue_link
                            inner join jira60.jiraissue incident_issue on (
                                issue_link.source = incident_issue.id
                                and issue_link.linktype in (11202, 11203, 11204) -- инцидент <-> аналитика, разработка, тестирование
                                and incident_issue.issuetype = 10412 --инцидент
                            )
                    ) issue_link on issue_link.destination = issue.id and issue_link.rank = 1 -- ограничить связь только с первым (по возрастанию id) инцидентом
                    inner join jira60.jiraissue incident_issue on issue_link.source = incident_issue.id and issue_link.linktype in (11202, 11203, 11204) -- инцидент <-> аналитика, разработка, тестирование
                where 
                    issue.issuetype in (12904, 12703, 10603) -- аналитика, разработка, тестирование
                order by 1
            """

            incident_sub_tasks = pd.read_sql(query, connection)

            incident_sub_task_not_specified = pd.DataFrame([[
                -1,
                "-1",
                "",
                "Не указано",
                -1,
                0,
                0,
                -1,
                "-1",
            ]], columns=[
                "id",
                "key",
                "url",
                "name",
                "skill_id",
                "time_left",
                "time_original_estimate",
                "incident_id",
                "state_id"
            ])

            incident_sub_tasks = incident_sub_tasks.append(
                incident_sub_task_not_specified,
                ignore_index=True
            )

            self.data = incident_sub_tasks

import pandas as pd

class TasksExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select
                    to_char(project.pkey||'-'||issue.issuenum) as "id",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                    issue.summary as "name",
                    CASE issue.issuetype
                        WHEN '12904' THEN 1
                        WHEN '12703' THEN 2
                        WHEN '10603' THEN 3
                    END as "skill_id",
                    CASE issue.issuetype
                        WHEN '12904' THEN analysis_hours_prelim_cv.numbervalue
                        WHEN '12703' THEN development_hours_prelim_cv.numbervalue
                        WHEN '10603' THEN testing_hours_prelim_cv.numbervalue
                    END as "preliminary_estimate",
                    CASE issue.issuetype
                        WHEN '12904' THEN analysis_hours_plan_cv.numbervalue
                        WHEN '12703' THEN development_hours_plan_cv.numbervalue
                        WHEN '10603' THEN testing_hours_plan_cv.numbervalue
                    END as "planned_estimate",
                    to_char(project.pkey)||'-'||system_change_request_issue.issuenum as "system_change_request_id",
                    issue.issuestatus as "state_id"
                from 
                    jira60.jiraissue issue
                    inner join jira60.project project on issue.project=project.id
                    left join jira60.customfieldvalue analysis_hours_prelim_cv on (analysis_hours_prelim_cv.issue = issue.id and analysis_hours_prelim_cv.customfield = 14636)
                    left join jira60.customfieldvalue development_hours_prelim_cv on (development_hours_prelim_cv.issue = issue.id and development_hours_prelim_cv.customfield = 15401)
                    left join jira60.customfieldvalue testing_hours_prelim_cv on (testing_hours_prelim_cv.issue = issue.id and testing_hours_prelim_cv.customfield = 15402)
                    left join jira60.customfieldvalue analysis_hours_plan_cv on (analysis_hours_plan_cv.issue = issue.id and analysis_hours_plan_cv.customfield = 15533)
                    left join jira60.customfieldvalue development_hours_plan_cv on (development_hours_plan_cv.issue = issue.id and development_hours_plan_cv.customfield = 15534)
                    left join jira60.customfieldvalue testing_hours_plan_cv on (testing_hours_plan_cv.issue = issue.id and testing_hours_plan_cv.customfield = 15535)
                    left join (
                        select
                            issue_link.*, (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank
                        from 
                            jira60.issuelink issue_link
                            inner join jira60.jiraissue system_change_request_issue on (
                                issue_link.source = system_change_request_issue.id
                                and issue_link.linktype in (11202, 11203, 11204) -- доработка системы <-> аналитика, разработка, тестирование
                                and system_change_request_issue.issuetype = 11901 --доработка системы
                            )
                    ) issue_link on issue_link.destination = issue.id and issue_link.rank = 1 -- ограничить связь только с первой (по возрастанию id) доработкой системы
                    inner join jira60.jiraissue system_change_request_issue on issue_link.source = system_change_request_issue.id and issue_link.linktype in (11202, 11203, 11204) -- доработка системы <-> аналитика, разработка, тестирование
                where 
                    issue.issuetype in (12904, 12703, 10603) -- аналитика, разработка, тестирование
                order by 1
            """

            tasks = pd.read_sql(query, connection)

            task_not_specified = pd.DataFrame([[
                "-1",
                "",
                "Не указано",
                -1,
                0,
                0,
                "-1",
                "-1",
            ]], columns=[
                "id",
                "url",
                "name",
                "skill_id",
                "preliminary_estimate",
                "planned_estimate",
                "system_change_request_id",
                "state_id"
            ])

            tasks = tasks.append(
                task_not_specified,
                ignore_index=True
            )

            self.data = tasks

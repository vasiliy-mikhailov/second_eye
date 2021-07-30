import pandas as pd

class TasksExtractor:
    def __init__(self, get_connection, last_period_number_of_days):
        self.get_connection = get_connection
        self.last_period_number_of_days = last_period_number_of_days

    def extract(self):
        get_connection = self.get_connection
        last_period_number_of_days = self.last_period_number_of_days

        with get_connection() as connection:
            query = """
                select
                    issue.id as "id",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                    issue.summary as "name",
                    CASE issue.issuetype
                        WHEN '12904' THEN 1
                        WHEN '12703' THEN 2
                        WHEN '10603' THEN 3
                    END as "skill_id",
                    CASE issue.issuetype
                        WHEN '12904' THEN 'Аналитика'
                        WHEN '12703' THEN 'Разработка'
                        WHEN '10603' THEN 'Тестирование'
                    END as "skill_name",
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
                    nvl(work_log.time_worked, 0) as "time_spent",
                    nvl(last_period_work_log.time_worked, 0) as "last_period_time_spent",
                    {} as "last_period_number_of_days",
                    system_change_request_issue.id as "system_change_request_id",
                    issue_status.pname as "state"
                from 
                    jira60.jiraissue issue
                    inner join jira60.project project on issue.project=project.id
                    left join jira60.issuestatus issue_status on issue.issuestatus = issue_status.id
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
                    ) issue_link on issue_link.destination = issue.id and issue_link.rank = 1 -- ограничить связь только с первой (по возрастанию id) доработкой системы
                    inner join jira60.jiraissue system_change_request_issue on issue_link.source = system_change_request_issue.id and issue_link.linktype in (11202, 11203, 11204) -- доработка системы <-> аналитика, разработка, тестирование
                    left join (select round(sum(work_log.timeworked) / 60 / 60) time_worked, work_log.issueid issue_id from jira60.worklog work_log group by work_log.issueid) work_log on work_log.issue_id = issue.id
                    left join (select round(sum(last_period_work_log.timeworked) / 60 / 60) time_worked, last_period_work_log.issueid issue_id from jira60.worklog last_period_work_log where startdate >= sysdate - {} group by last_period_work_log.issueid) last_period_work_log on last_period_work_log.issue_id = issue.id
                where 
                    issue.issuetype in (12904, 12703, 10603) -- аналитика, разработка, тестирование
                order by 1
            """.format(last_period_number_of_days, last_period_number_of_days)

            tasks = pd.read_sql(query, connection, index_col="id")

            self.data = tasks
import pandas as pd

class SystemChangeRequestsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select distinct
                    issue.id as "id",
                    project.pkey||'-'||issue.issuenum as "key",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                    issue.summary as "name",
                    to_number(system_cv_id.stringValue) as "system_id",
                    analysis_hours_prelim_cv.numbervalue as "analysis_preliminary_estimate",
                    dev_preliminary_estimate_cv.numbervalue as "dev_preliminary_estimate",
                    testing_hours_prelim_cv.numbervalue as "testing_preliminary_estimate",
                    analysis_hours_plan_cv.numbervalue as "analysis_planned_estimate",
                    dev_planned_estimate_cv.numbervalue as "dev_planned_estimate",
                    testing_hours_plan_cv.numbervalue as "testing_planned_estimate",
                    change_request_issue.id as "change_request_id",
                    issue.issuestatus as "state_id"
                from 
                    jira60.jiraissue issue
                    inner join jira60.project project on issue.project=project.id
                    left join jira60.customfieldvalue system_cv_id on (system_cv_id.issue = issue.id and system_cv_id.customfield = 14713)
                    left join jira60.customfieldvalue analysis_hours_prelim_cv on (analysis_hours_prelim_cv.issue = issue.id and analysis_hours_prelim_cv.customfield = 14636)
                    left join jira60.customfieldvalue dev_preliminary_estimate_cv on (dev_preliminary_estimate_cv.issue = issue.id and dev_preliminary_estimate_cv.customfield = 15401)
                    left join jira60.customfieldvalue testing_hours_prelim_cv on (testing_hours_prelim_cv.issue = issue.id and testing_hours_prelim_cv.customfield = 15402)
                    left join jira60.customfieldvalue analysis_hours_plan_cv on (analysis_hours_plan_cv.issue = issue.id and analysis_hours_plan_cv.customfield = 15533)
                    left join jira60.customfieldvalue dev_planned_estimate_cv on (dev_planned_estimate_cv.issue = issue.id and dev_planned_estimate_cv.customfield = 15534)
                    left join jira60.customfieldvalue testing_hours_plan_cv on (testing_hours_plan_cv.issue = issue.id and testing_hours_plan_cv.customfield = 15535)
                    left join (
                        select
                            issue_link.*, (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank
                        from 
                            jira60.issuelink issue_link
                            inner join jira60.jiraissue change_request_issue on (
                                issue_link.source = change_request_issue.id
                                and issue_link.linktype = 10405
                                and change_request_issue.issuetype=11900
                            )
                    ) issue_link on issue_link.destination = issue.id and issue_link.rank = 1 -- ограничить связь только с первой (по возрастанию id) заявкой на доработку
                    inner join jira60.jiraissue change_request_issue on issue_link.source = change_request_issue.id and issue_link.linktype = 10405 -- заявка на доработку ПО <-> заявка на доработку системы
                where 
                    issue.issuetype = 11901 --доработка системы
            """

            system_change_requests = pd.read_sql(query, connection)
            system_change_requests['system_id'].fillna(-1, inplace=True)

            system_change_request_not_specified = pd.DataFrame([[
                -1,
                "-1",
                "",
                "Не указано",
                -1,
                0,
                0,
                0,
                0,
                0,
                0,
                -1,
                "-1",
            ]], columns=[
                "id",
                "key",
                "url",
                "name",
                "system_id",
                "analysis_preliminary_estimate",
                "dev_preliminary_estimate",
                "testing_preliminary_estimate",
                "analysis_planned_estimate",
                "dev_planned_estimate",
                "testing_planned_estimate",
                "change_request_id",
                "state_id",
            ])

            system_change_requests = system_change_requests.append(
                system_change_request_not_specified,
                ignore_index=True
            )

            system_change_requests.rename(columns={
                "dev_preliminary_estimate": "development_preliminary_estimate",
                "dev_planned_estimate": "development_planned_estimate",
            }, inplace=True)

            self.data = system_change_requests
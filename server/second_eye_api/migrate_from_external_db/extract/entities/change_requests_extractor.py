import pandas as pd

class ChangeRequestsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                    select
                        project.pkey||'-'||issue.issuenum as "id",
                        'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                        issue.summary as "name",
                        analysis_hours_express_cv.numbervalue + dev_express_estimate_cv.numbervalue + testing_hours_express_cv.numbervalue as "express_estimate",
                        analysis_hours_express_cv.numbervalue as "analysis_express_estimate",
                        dev_express_estimate_cv.numbervalue as "development_express_estimate",
                        testing_hours_express_cv.numbervalue as "testing_express_estimate",
                        issue.issuestatus as "state_id",
                        to_char(planned_install_date_cfv.datevalue, 'YYYY-MM-DD') as "planned_install_date",
                        nvl(year_label.year, -1) as "year_label_max",
                        to_number(issue_project_team.stringvalue) as "project_team_id",
                        case nvl(to_number(issue_goal.stringValue), 0)
                            when 15318 then 0 -- автоматизация процесса
                            else 1
                        end as "has_value"
                    from 
                        jira60.jiraissue issue
                        inner join jira60.project project on issue.project=project.id
                        left join jira60.customfieldvalue analysis_hours_express_cv on (analysis_hours_express_cv.issue = issue.id and analysis_hours_express_cv.customfield = 14809)
                        left join jira60.customfieldvalue dev_express_estimate_cv on (dev_express_estimate_cv.issue = issue.id and dev_express_estimate_cv.customfield = 14810)
                        left join jira60.customfieldvalue testing_hours_express_cv on (testing_hours_express_cv.issue = issue.id and testing_hours_express_cv.customfield = 14811)
                        left join jira60.customfieldvalue planned_install_date_cfv on planned_install_date_cfv.issue=issue.id and planned_install_date_cfv.customfield=14615 
                        left join (
                            select
                                to_number(regexp_substr(label,'\dквартал(\d+)$', 1, 1, NULL, 1)) as year,
                                label.issue,
                                (ROW_NUMBER() OVER(PARTITION BY issue ORDER BY to_number(regexp_substr(label,'\dквартал(\d+)$', 1, 1, NULL, 1)) desc)) as rank
                            from 
                                jira60.label
                            where
                                regexp_like(label.label, '\dквартал(\d+)$')                               
                        ) year_label on (year_label.issue=issue.id and year_label.rank = 1) -- Первая метка с максимальным годом
                        left join jira60.customFieldValue issue_project_team on issue_project_team.issue = issue.id and issue_project_team.customfield=17127 and issue_project_team.parentkey is not null --'Команда проекта
                        left join jira60.customFieldValue issue_goal on issue_goal.issue = issue.id and issue_goal.customField=14622
                    where 
                        issue.issuetype=11900 --заявка на доработку ПО
        """

            change_requests = pd.read_sql(
                query,
                connection,
                parse_dates={"planned_install_date"}
            )
            change_requests['project_team_id'].fillna(-1, inplace=True)
            change_requests["planned_install_date"] = change_requests["planned_install_date"].dt.date

            change_request_not_specified = pd.DataFrame([[
                -1,
                "",
                "Не указано",
                0,
                0,
                0,
                0,
                -1,
                None,
                -1,
                -1,
                0
            ]], columns=[
                "id",
                "url",
                "name",
                "express_estimate",
                "analysis_express_estimate",
                "development_express_estimate",
                "testing_express_estimate",
                "state_id",
                "planned_install_date",
                "year_label_max",
                "project_team_id",
                "has_value"
            ])
            change_requests = change_requests.append(
                change_request_not_specified
            )

            self.data = change_requests
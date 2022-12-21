import pandas as pd

class ChangeRequestsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                    select
                        issue.id as "id",
                        project.pkey||'-'||issue.issuenum as "key",
                        'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as "url",
                        issue.summary as "name",
                        analysis_hours_express_cv.numbervalue as "analysis_express_estimate",
                        dev_express_estimate_cv.numbervalue as "development_express_estimate",
                        testing_hours_express_cv.numbervalue as "testing_express_estimate",
                        issue.issuestatus as "state_id",
                        to_char(install_date_cfv.datevalue, 'YYYY-MM-DD') as "install_date",
                        resolutiondate as "resolution_date",
                        to_char(planned_install_date_cfv.datevalue, 'YYYY-MM-DD') as "planned_install_date",
                        nvl(year_label.year, -1) as "year_label_max",
                        to_number(issue_project_team.stringvalue) as "project_team_id",
                        case nvl(to_number(issue_goal.stringValue), 0)
                            when 15318 then 0 -- автоматизация процесса
                            else 1
                        end as "has_value",
                        case nvl(to_number(issue_goal.stringValue), 0)
                            when 27319 then 1 -- технологическое перевооружение
                            when 23732 then 1 -- исправление проблемы
                            else 0
                        end as "is_reengineering",
                        nvl(epic_issue_data.id, -1) as "epic_id",
                        case nvl(to_number(quarter_cfv.stringValue), '-1')
                            when 488701 then '2022-I'
                            when 504375 then '2022-I'
                            when 488702 then '2022-II'
                            when 504238 then '2022-II'
                            when 488703 then '2022-III'
                            when 504239 then '2022-III'
                            when 488704 then '2022-IV'
                            when 504240 then '2022-IV'
                            when 600070 then '2023-I'
                            when 600080 then '2023-I'
                            when 638563 then '2023-II'
                            when 638565 then '2023-II'
                            when 638569 then '2023-III'
                            when 638571 then '2023-III'
                            when 638573 then '2023-IV'
                            when 638574 then '2023-IV'
                            else '-1'
                        end as "quarter_key"
                    from 
                        jira60.jiraissue issue
                        inner join jira60.project project on issue.project=project.id
                        left join jira60.customfieldvalue analysis_hours_express_cv on (analysis_hours_express_cv.issue = issue.id and analysis_hours_express_cv.customfield = 14809)
                        left join jira60.customfieldvalue dev_express_estimate_cv on (dev_express_estimate_cv.issue = issue.id and dev_express_estimate_cv.customfield = 14810)
                        left join jira60.customfieldvalue testing_hours_express_cv on (testing_hours_express_cv.issue = issue.id and testing_hours_express_cv.customfield = 14811)
                        left join jira60.customfieldvalue planned_install_date_cfv on planned_install_date_cfv.issue=issue.id and planned_install_date_cfv.customfield = 14615
                        left join jira60.customfieldvalue install_date_cfv on install_date_cfv.issue=issue.id and install_date_cfv.customfield = 14619 
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
                        left join jira60.customFieldValue issue_project_team on issue_project_team.issue = issue.id and issue_project_team.customfield = 17127 and issue_project_team.parentkey is not null --'Команда проекта
                        left join jira60.customFieldValue issue_goal on issue_goal.issue = issue.id and issue_goal.customField = 14622
                        left join (
                            select
                                epic_issue_link.destination,
                                (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank,
                                epic_issue.id
                            from 
                                jira60.issuelink epic_issue_link
                                inner join jira60.jiraissue epic_issue on (
                                    epic_issue_link.source = epic_issue.id
                                    and epic_issue_link.linktype = 10800 -- Epic -> доработка системы
                                    and epic_issue.issuetype = 11007 -- Epic
                                )
                        ) epic_issue_data on epic_issue_data.destination = issue.id and epic_issue_data.rank = 1 -- ограничить связь только с первой (по возрастанию id) доработкой системы
                        left join jira60.customFieldValue quarter_cfv on quarter_cfv.issue=issue.id and quarter_cfv.customField = 17740 
                    where 
                        issue.issuetype = 11900 --заявка на доработку ПО
        """

            change_requests = pd.read_sql(
                query,
                connection,
                parse_dates={"install_date", "resolution_date", "planned_install_date"}
            )
            change_requests['project_team_id'].fillna(-1, inplace=True)

            change_requests["install_date"] = change_requests["install_date"].dt.date
            change_requests["resolution_date"] = change_requests["resolution_date"].dt.date
            change_requests["planned_install_date"] = change_requests["planned_install_date"].dt.date

            change_request_not_specified = pd.DataFrame([[
                -1,
                "-1",
                "",
                "Не указано",
                0,
                0,
                0,
                "-1",
                None,
                -1,
                -1,
                0,
                0,
                -1,
                "-1",
                None,
                None
            ]], columns=[
                "id",
                "key",
                "url",
                "name",
                "analysis_express_estimate",
                "development_express_estimate",
                "testing_express_estimate",
                "state_id",
                "planned_install_date",
                "year_label_max",
                "project_team_id",
                "has_value",
                "is_reengineering",
                "epic_id",
                "quarter_key",
                "install_date",
                "resolution_date"
            ])
            change_requests = change_requests.append(
                change_request_not_specified,
                ignore_index=True
            )

            self.data = change_requests
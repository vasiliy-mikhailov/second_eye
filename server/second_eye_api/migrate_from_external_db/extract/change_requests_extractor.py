import pandas as pd

class ChangeRequestsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select
                    id as "id",
                    url as "url",
                    name as "name",
                    analysis_express_estimate + development_express_estimate + testing_express_estimate as "express_estimate",
                    analysis_express_estimate as "analysis_express_estimate",
                    development_express_estimate as "development_express_estimate",
                    testing_express_estimate as "testing_express_estimate", 
                    state as "state",
                    planned_install_date "planned_install_date",
                    count(this_year_quarter_label) as "this_year_quarter_label_count",
                    project_team_id as "project_team_id",
                    dedicated_team_id as "dedicated_team_id"
                from (
                    select
                        issue.id as id,
                        'https://jira.mcb.ru/browse/'||project.pkey||'-'||issue.issuenum as url,
                        issue.summary as name,
                        analysis_hours_express_cv.numbervalue as analysis_express_estimate,
                        dev_express_estimate_cv.numbervalue as development_express_estimate,
                        testing_hours_express_cv.numbervalue as testing_express_estimate,
                        issue_status.pname as state,
                        planned_install_date_cfv.datevalue as planned_install_date,
                        this_year_quarter_label_table.label as this_year_quarter_label,
                        to_number(issue_project_team.stringvalue) as project_team_id,
                        to_number(issue_dedicated_team.stringvalue) as dedicated_team_id
                    from 
                        jira60.jiraissue issue
                        inner join jira60.project project on issue.project=project.id
                        left join jira60.issuestatus issue_status on issue.issuestatus = issue_status.id
                        left join jira60.customfieldvalue analysis_hours_express_cv on (analysis_hours_express_cv.issue = issue.id and analysis_hours_express_cv.customfield = 14809)
                        left join jira60.customfieldvalue dev_express_estimate_cv on (dev_express_estimate_cv.issue = issue.id and dev_express_estimate_cv.customfield = 14810)
                        left join jira60.customfieldvalue testing_hours_express_cv on (testing_hours_express_cv.issue = issue.id and testing_hours_express_cv.customfield = 14811)
                        left join jira60.issuelink issue_link on issue_link.destination=issue.id
                        left join jira60.customfieldvalue planned_install_date_cfv on planned_install_date_cfv.issue=issue.id and planned_install_date_cfv.customfield=14615 
                        left join jira60.label this_year_quarter_label_table on (this_year_quarter_label_table.issue=issue.id and this_year_quarter_label_table.label like '_кв%2021')
                        left join jira60.customfieldvalue issue_project_team on issue_project_team.issue = issue.id and issue_project_team.customfield=17127 and issue_project_team.parentkey is not null --'Команда руководителя проекта
                        left join jira60.customfieldvalue issue_dedicated_team on issue_dedicated_team.issue = issue.id and issue_dedicated_team.customfield=17127 and issue_dedicated_team.parentkey is null --'Команда бизнес партнера проекта
                    where 
                        issue.issuetype=11900 --заявка на доработку ПО
                ) t
                group by
                  id, url, name,
                  analysis_express_estimate + development_express_estimate + testing_express_estimate,
                  analysis_express_estimate, development_express_estimate, testing_express_estimate, 
                  state, planned_install_date, project_team_id, dedicated_team_id
                order by
                  id
        """

            change_requests = pd.read_sql(
                query,
                connection,
                index_col="id",
                parse_dates={"planned_install_date"}
            )
            change_requests['project_team_id'].fillna(-1, inplace=True)
            change_requests['dedicated_team_id'].fillna(-1, inplace=True)
            change_request_not_specified = pd.DataFrame([[
                -1,
                "",
                "Не указано",
                0,
                0,
                0,
                0,
                "Запланировано",
                pd.Timestamp.now(),
                1,
                -1,
                -1
            ]], columns=[
                "id",
                "url",
                "name",
                "express_estimate",
                "analysis_express_estimate",
                "development_express_estimate",
                "testing_express_estimate",
                "state",
                "planned_install_date",
                "this_year_quarter_label_count",
                "project_team_id",
                "dedicated_team_id"

            ])
            change_requests = change_requests.reset_index().append(
                change_request_not_specified
            )

            self.data = change_requests


"""
"""
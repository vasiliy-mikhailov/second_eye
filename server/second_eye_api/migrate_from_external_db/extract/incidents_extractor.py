import pandas as pd

class IncidentsExtractor:
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
                    nvl(to_number(system_cv_id.stringValue), -1) as "system_id",
                    issue.issuestatus as "state_id",
                    to_char(install_date_cfv.datevalue, 'YYYY-MM-DD') as "install_date",
                    resolutiondate as "resolution_date",
                    to_char(planned_install_date_cfv.datevalue, 'YYYY-MM-DD') as "planned_install_date",
                    nvl(year_label.year, -1) as "year_label_max",
                    to_number(issue_project_team.stringvalue) as "project_team_id"
                from 
                    jira60.jiraissue issue
                    inner join jira60.project project on issue.project=project.id
                    left join jira60.customfieldvalue system_cv_id on (system_cv_id.issue = issue.id and system_cv_id.customfield = 14713)
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
                where 
                    issue.issuetype = 10412 --инцидент
                    and project.pkey = 'MKB'
        """

            incidents = pd.read_sql(
                query,
                connection,
                parse_dates={"install_date", "resolution_date", "planned_install_date"}
            )
            incidents['project_team_id'].fillna(-1, inplace=True)

            incidents["install_date"] = incidents["install_date"].dt.date
            incidents["resolution_date"] = incidents["resolution_date"].dt.date
            incidents["planned_install_date"] = incidents["planned_install_date"].dt.date

            self.data = incidents
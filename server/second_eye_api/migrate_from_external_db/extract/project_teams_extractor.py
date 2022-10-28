import pandas as pd

class ProjectTeamsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection

        with get_connection() as connection:
            query = """
                select 
                    project_team_cfo.id as "id",
                    project_team_cfo.parentoptionid as "dedicated_team_id",
                    project_team_cfo.customValue as "name",
                    'https://jira.mcb.ru/browse/MKBTEAM-'||project_team_issue.issuenum as "url",
                    1 as "company_id",
                    nvl(project_team_issue.project_manager_id, '-1') as "project_manager_key"
                from 
                    jira60.customFieldOption project_team_cfo
                    left join (
                        select
                            to_number(project_team_cfv.stringValue) project_team_id,
                            -- lower(project_manager_cfv.stringValue) project_manager_id,
                            project_team_issue.assignee project_manager_id,
                            project_team_issue.issuenum,
                            (ROW_NUMBER() OVER(PARTITION BY project_team_cfv.stringValue ORDER BY project_team_issue.id)) as rank
                        from
                            jira60.customFieldValue project_team_cfv,
                            jira60.jiraissue project_team_issue
                            left join jira60.customFieldValue project_manager_cfv on project_manager_cfv.issue=project_team_issue.id and project_manager_cfv.customField=17108 --Руководитель проекта
                        where
                            project_team_issue.issuetype = 13203 -- Команда проекта
                            and project_team_cfv.issue = project_team_issue.id
                            and project_team_cfv.customField = 17127
                            and project_team_cfv.parentKey is not null
                    ) project_team_issue on (project_team_cfo.id = project_team_issue.project_team_id and project_team_issue.rank = 1)
                where
                    project_team_cfo.customField = 17127
                    and project_team_cfo.parentOptionId is not null
            """

            project_teams = pd.read_sql(query, connection)
            project_team_not_specified = pd.DataFrame(
                [[-1, -1, "Не указано", "", 1, "-1"]],
                columns=["id", "dedicated_team_id", "name", "url", "company_id", "project_manager_key"]
            )
            project_teams = project_teams.append(
                project_team_not_specified,
                sort=False,
                ignore_index=True
            )

            self.data = project_teams
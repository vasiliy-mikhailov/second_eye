import pandas as pd

class DedicatedTeamsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select 
                    dedicated_team_cfo.id as "id",
                    dedicated_team_cfo.customValue as "name",
                    1 as "company_id",
                    nvl(dedicated_team_issue.cio_key, '-1') as "cio_key",
                    nvl(dedicated_team_issue.cto_key, '-1') as "cto_key"
                from 
                    jira60.customFieldOption dedicated_team_cfo
                    left join (
                        select
                            to_number(dedicated_team_cfv.stringValue) dedicated_team_id,
                            lower(cio_cfv.stringValue) cio_key,
                            lower(cto_cfv.stringValue) cto_key,
                            (ROW_NUMBER() OVER(PARTITION BY dedicated_team_cfv.stringValue ORDER BY dedicated_team_issue.id)) as rank
                        from
                            jira60.customFieldValue dedicated_team_cfv,
                            jira60.jiraissue dedicated_team_issue
                            left join jira60.customFieldValue cio_cfv on cio_cfv.issue=dedicated_team_issue.id and cio_cfv.customField=17106 --Бизнес-партнер
                            left join jira60.customFieldValue cto_cfv on cto_cfv.issue=dedicated_team_issue.id and cto_cfv.customField=17107 --Руководитель разработки
                        where
                            dedicated_team_issue.issuetype = 13202 -- Выделенная команда
                            and dedicated_team_cfv.issue = dedicated_team_issue.id
                            and dedicated_team_cfv.customField = 17127
                            and dedicated_team_cfv.parentKey is null
                    ) dedicated_team_issue on (dedicated_team_cfo.id = dedicated_team_issue.dedicated_team_id and dedicated_team_issue.rank = 1)
                where
                    dedicated_team_cfo.customField = 17127
                    and dedicated_team_cfo.parentOptionId is null
            """

            data = pd.read_sql(query, connection)
            dedicated_team_not_specified = pd.DataFrame([[-1, "Не указано", 1, "-1", "-1"]], columns=["id", "name", "company_id", "cio_key", "cto_key"])
            data = data.append(
                dedicated_team_not_specified,
                sort=False,
                ignore_index=True
            )

            self.data = data

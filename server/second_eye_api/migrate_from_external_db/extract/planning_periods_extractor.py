import pandas as pd

class PlaningPeriodsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select distinct
                    to_number(id) as "id"
                from (
                    select distinct
                        nvl(extract(year from planned_install_date_cfv.datevalue), -1) as id
                    from 
                        jira60.jiraissue issue
                        left join jira60.customfieldvalue planned_install_date_cfv on planned_install_date_cfv.issue=issue.id and planned_install_date_cfv.customfield = 14615 
                    where 
                        issue.issuetype = 11900 --заявка на доработку ПО
                    union all
                    select distinct
                        nvl(extract(year from install_date_cfv.datevalue), -1) as id
                    from 
                        jira60.jiraissue issue
                        left join jira60.customfieldvalue install_date_cfv on install_date_cfv.issue=issue.id and install_date_cfv.customfield = 14619 
                    where 
                        issue.issuetype = 11900 --заявка на доработку ПО
                    union all 
                    select distinct
                        nvl(extract(year from resolutiondate), -1) as id
                    from 
                        jira60.jiraissue issue
                    where 
                        issue.issuetype=11900 --заявка на доработку ПО
                    union all
                    select distinct
                        nvl(to_number(regexp_substr(label,'\dквартал(\d+)$', 1, 1, NULL, 1)), -1) as id
                    from 
                        jira60.jiraissue issue 
                        left join jira60.label year_label on year_label.issue=issue.id
                    where 
                        issue.issuetype = 11900 --заявка на доработку ПО                    
                    union all
                    select
                        -1
                    from
                        dual
                )
        """

            planning_periods = pd.read_sql(
                query,
                connection,
            )

            self.data = planning_periods


"""
"""
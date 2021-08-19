import pandas as pd

class ProjectTeamPositionAbilitiesExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select distinct
                    ability.id as "id",
                    'https://jira.mcb.ru/browse/MKBTEAM-'||ability.issuenum as "url",
                    ability.summary as "name",
                    to_number(system_cv_id.stringValue) as "system_id",
                    position.id as "project_team_position_id",
                    case to_number(skill_cv_id.stringValue)
                        when 25269 then 1 -- Аналитика
                        when 25270 then 2 -- Разработка
                        when 25271 then 3 -- Тестирование
                        else -1
                    end as "skill_id"
                from
                    jira60.jiraissue ability
                    left join jira60.issuelink position_link on position_link.destination=ability.id and position_link.linktype=10100
                    left join jira60.jiraissue position on position.id = position_link.source and position.issuetype=13205
                    left join jira60.issuelink team_link on team_link.source=position.id and team_link.linktype = 11600
                    right join jira60.jiraissue team on team.id = team_link.destination and team.issuetype = 13203 -- Проектная команда
                    left join jira60.customFieldValue system_cv_id on (system_cv_id.issue = ability.id and system_cv_id.customField = 14713)
                    left join jira60.customFieldValue skill_cv_id on (skill_cv_id.issue = ability.id and skill_cv_id.customField=17110)
                    inner join jira60.customFieldValue team_cfv on team_cfv.issue=team.id and team_cfv.parentkey is not null and team_cfv.customField=17127 -- Бизнес-команда
                where
                    ability.issuetype=13204
            """

            project_team_position_abilities = pd.read_sql(query, connection)
            project_team_position_abilities = project_team_position_abilities.drop_duplicates(subset=['id'])

            self.data = project_team_position_abilities
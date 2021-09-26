import pandas as pd

class ProjectTeamPositionsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select distinct
                    position.id as "id",
                    'https://jira.mcb.ru/browse/MKBTEAM-'||position.issuenum as "url",
                    position.summary as "name",
                    incident_capacity_cfv.numberValue as "incident_capacity",
                    management_capacity_cfv.numberValue as "management_capacity",
                    change_request_capacity_cfv.numberValue as "change_request_capacity",
                    other_capacity_cfv.numberValue as "other_capacity",
                    case 
                        when person_issue.project = 14200 then lower(outsource_person_cfv.stringValue)
                        when person_issue.project = 15306 then lower(insource_person_cfv.stringValue)
                    end as "person_id",
                    team_cfv.stringValue as "project_team_id"
                from 
                    jira60.jiraissue position
                    left join jira60.customFieldValue incident_capacity_cfv on (incident_capacity_cfv.issue=position.id and incident_capacity_cfv.customfield=17114) --Часов на инциденты в день (план)
                    left join jira60.customFieldValue management_capacity_cfv on (management_capacity_cfv.issue=position.id and management_capacity_cfv.customfield=17116) --Часов на управление в день (план)
                    left join jira60.customFieldValue change_request_capacity_cfv on (change_request_capacity_cfv.issue=position.id and change_request_capacity_cfv.customfield=17113) --Часов на доработки в день (план)
                    left join jira60.customFieldValue other_capacity_cfv on (other_capacity_cfv.issue=position.id and other_capacity_cfv.customfield=17115) --Часов на прочее в день (план)
                    left join jira60.customFieldValue person_cfv on person_cfv.issue=position.id and person_cfv.customfield=17111 --Исполнитель МКБ/аутсорсинговой компании
                    left join jira60.jiraissue person_issue on person_issue.id=to_number(person_cfv.stringValue)
                    left join jira60.customFieldValue outsource_person_cfv on outsource_person_cfv.issue=person_issue.id and outsource_person_cfv.customfield=15642 and person_issue.project=14200 --Логин MKBOUT
                    left join jira60.customFieldValue insource_person_cfv on insource_person_cfv.issue=person_issue.id and insource_person_cfv.customfield=17120 and person_issue.project=15306 --Пользователь (логин MKB)
                    left join jira60.issuelink team_link on team_link.source=position.id and team_link.linktype in (11600)
                    inner join jira60.jiraissue team on team.id = team_link.destination and team.issuetype = 13203 -- Команда проекта
                    inner join jira60.customFieldValue team_cfv on team_cfv.issue=team.id and team_cfv.parentkey is not null and team_cfv.customField=17127 -- Бизнес-команда
                where
                    position.issuetype=13205
            """

            project_team_positions = pd.read_sql(query, connection)
            project_team_positions = project_team_positions.drop_duplicates(subset=['id'])

            self.data = project_team_positions
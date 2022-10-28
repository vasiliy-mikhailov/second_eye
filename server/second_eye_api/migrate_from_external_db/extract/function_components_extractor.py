import pandas as pd

class FunctionComponentsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select 
                    function_component.id as "id",
                    project.pkey||'-'||function_component.issuenum as "key",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||function_component.issuenum as "url",
                    function_component.summary as "name",
                    function_component_status.id as "state_id",
                    development_task.id as "task_id",
                    case function_component_kind.stringvalue
                        when '23966' then 1 -- вход
                        when '23967' then 2 -- выход
                        when '23968' then 3 -- таблица
                        when '23969' then 4 -- сообщение
                        when '23970' then 5 -- интерфейс
                    end "kind_id",
                    nvl(function_component_count_cv.numberValue, 1) as "count"
                from
                    jira60.jiraissue function_component
                    inner join jira60.project project on function_component.project=project.id
                    left join jira60.issuestatus function_component_status on function_component.issuestatus = function_component_status.id
                    inner join (
                        select
                            issue_link.*, (ROW_NUMBER() OVER(PARTITION BY destination ORDER BY destination)) as rank
                        from 
                            jira60.issuelink issue_link
                            inner join jira60.jiraissue development_task on (
                                issue_link.source = development_task.id
                                and issue_link.linktype = 11401 -- функциональная компонента -> задача
                                and development_task.issuetype = 12703 -- разработка
                            )
                    ) issue_link on issue_link.destination = function_component.id and issue_link.rank = 1  -- -- ограничить связь только с первой (по возрастанию id) задачей
                    inner join jira60.jiraissue development_task on issue_link.source = development_task.id and issue_link.linktype = 11401 -- задача
                    inner join jira60.customFieldValue function_component_kind on function_component_kind.issue=function_component.id and function_component_kind.customField = 16246 -- тип функциональной компоненты
                    left join jira60.customFieldValue function_component_count_cv on function_component_count_cv.issue=function_component.id and function_component_count_cv.customField = 16286 -- количество функциональных компонент
                where
                    function_component.issuetype = 13101 -- функциональная компонента
            """
            function_components = pd.read_sql(query, connection)

            self.data = function_components
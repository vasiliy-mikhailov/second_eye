import pandas as pd

class FunctionComponentsExtractor:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        get_connection = self.get_connection
        with get_connection() as connection:
            query = """
                select 
                    project.pkey||'-'||function_component.issuenum as "id",
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||function_component.issuenum as "url",
                    function_component.summary as "name",
                    function_component_status.id as "state_id",
                    project.pkey||'-'||development_task.issuenum as "task_id",
                    case function_component_kind.stringvalue
                        when '23966' then 1 -- вход
                        when '23967' then 2 -- выход
                        when '23968' then 3 -- таблица
                        when '23969' then 4 -- сообщение
                        when '23970' then 5 -- интерфейс
                    end "kind_id",
                    function_component_count_cv.numberValue as "count"
                from
                    jira60.jiraissue function_component
                    inner join jira60.project project on function_component.project=project.id
                    left join jira60.issuestatus function_component_status on function_component.issuestatus = function_component_status.id
                    inner join jira60.issuelink link on (link.destination = function_component.id and link.linkType = 11401) -- Функциональная компонента -> Задача
                    inner join jira60.jiraissue development_task on (link.source = development_task.id and development_task.issuetype = 12703) -- разработка
                    inner join jira60.customFieldValue function_component_kind on function_component_kind.issue=function_component.id and function_component_kind.customField=16246 -- тип функциональной компоненты
                    inner join jira60.customFieldValue function_component_count_cv on function_component_count_cv.issue=function_component.id and function_component_count_cv.customField=16286 -- количество функциональных компонент
                where
                    function_component.issuetype = 13101 -- функциональная компонента
            """
            function_components = pd.read_sql(query, connection)

            self.data = function_components
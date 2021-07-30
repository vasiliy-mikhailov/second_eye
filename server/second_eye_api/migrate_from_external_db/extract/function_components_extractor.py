class ExtractFunctionComponents:
    def __init__(self, get_connection):
        self.get_connection = get_connection

    def extract(self):
        with get_connection() as connection:
            query = """
                select 
                    function_component.id,
                    'https://jira.mcb.ru/browse/'||project.pkey||'-'||function_component.issuenum as url,
                    function_component.summary name,
                    function_component_status.pname as state,
                    development_task.id task_id,
                    case function_component_type.stringvalue
                        when '23966' then 4 -- вход
                        when '23967' then 5 -- выход
                        when '23968' then 10 -- таблица
                        when '23969' then 4 -- сообщение
                        when '23970' then 7 -- интерфейс
                    end function_component_type_weight,
                    function_component_type_name.customvalue as function_component_type_id,
                    function_component_count_cv.numberValue count
                from
                    jira60.jiraissue function_component
                    inner join jira60.project project on function_component.project=project.id
                    left join jira60.issuestatus function_component_status on function_component.issuestatus = function_component_status.id
                    inner join jira60.issuelink link on (link.destination = function_component.id and link.linkType = 11401) -- Функциональная компонента -> Разработка
                    inner join jira60.jiraissue development_task on (link.source = development_task.id and development_task.issuetype = 12703) -- разработка
                    inner join jira60.customFieldValue function_component_type on function_component_type.issue=function_component.id and function_component_type.customField=16246 -- тип функциональной компоненты
                    inner join jira60.customFieldOption function_component_type_name on function_component_type_name.Id=to_number(function_component_type.stringValue) and function_component_type_name.customField=function_component_type.customField
                    inner join jira60.customFieldValue function_component_count_cv on function_component_count_cv.issue=function_component.id and function_component_count_cv.customField=16286 -- количество функциональных компонент
                where
                    function_component.issuetype = 13101 -- функциональная компонента
            """
            function_components = pd.read_sql(query, connection, index_col="ID")

            self.data = function_components
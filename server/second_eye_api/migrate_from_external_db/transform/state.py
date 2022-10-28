import cubista

class State(cubista.Table):
    STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING = {
        'Черновик': lambda: StateCategory.TODO,
        'Новая': lambda: StateCategory.TODO,
        'Анализ инициативы': lambda: StateCategory.TODO,
        'Запланировано': lambda: StateCategory.TODO,
        'Предварительно согласовано ДИБ': lambda: StateCategory.TODO,
        'Предварительное согласование ДИБ': lambda: StateCategory.TODO,
        'Открыто': lambda: StateCategory.TODO,
        'Оценка проведена': lambda: StateCategory.TODO,
        'Оценка в ДИТ': lambda: StateCategory.TODO,
        'Согласование ДИБ': lambda: StateCategory.TODO,
        'Согласовано ДИБ': lambda: StateCategory.TODO,
        'Аналитика': lambda: StateCategory.IN_PROGRESS,
        'Готово к разработке': lambda: StateCategory.IN_PROGRESS,
        'Разработка': lambda: StateCategory.IN_PROGRESS,
        'Разработка тест-кейсов': lambda: StateCategory.IN_PROGRESS,
        'Готово к тестированию': lambda: StateCategory.IN_PROGRESS,
        'Тестирование': lambda: StateCategory.IN_PROGRESS,
        'Test тестирование': lambda: StateCategory.IN_PROGRESS,
        'В работе': lambda: StateCategory.IN_PROGRESS,
        'Опытно-промышленная эксплуатация': lambda: StateCategory.IN_PROGRESS,
        'Code review': lambda: StateCategory.IN_PROGRESS,
        'Preprod тестирование': lambda: StateCategory.IN_PROGRESS,
        'Готова к переносу на ПРОД': lambda: StateCategory.IN_PROGRESS,
        'Выполнена': lambda: StateCategory.DONE,
        'Выполнено': lambda: StateCategory.DONE,
        'Закрыто': lambda: StateCategory.DONE,
        'Завершена': lambda: StateCategory.DONE,
        'Отменено': lambda: StateCategory.DONE,
        'Отложено': lambda: StateCategory.DONE,
        'Не согласовано ДИБ': lambda: StateCategory.DONE
    }

    CANCELLED_STATES = [
        "Отменено",
        "Не согласовано ДИБ"
    ]

    class Fields:
        id = cubista.StringField(primary_key=True, unique=True)
        name = cubista.StringField()
        category_id = cubista.CalculatedField(
            lambda_expression=lambda x:
                State.STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING[x["name"]]()
                if x["name"] in State.STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING
                else -1
            ,
            source_fields=["name"]
        )
        is_cancelled = cubista.CalculatedField(
            lambda_expression=lambda x: x["name"] in State.CANCELLED_STATES,
            source_fields=["name"]
        )

class StateCategory(cubista.Table):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3
    NOT_SET = -1

    class Fields:
        id = cubista.IntField(primary_key=True, unique=True)
        name = cubista.StringField()
from second_eye_api.models import StateCategory

def calculate_state_category_for_states_inplace(states):
    STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING = {
        'Черновик': StateCategory.TODO,
        'Новая': StateCategory.TODO,
        'Анализ инициативы': StateCategory.TODO,
        'Запланировано': StateCategory.TODO,
        'Предварительно согласовано ДИБ': StateCategory.TODO,
        'Предварительное согласование ДИБ': StateCategory.TODO,
        'Открыто': StateCategory.TODO,
        'Оценка проведена': StateCategory.TODO,
        'Оценка в ДИТ': StateCategory.TODO,
        'Согласование ДИБ': StateCategory.TODO,
        'Согласовано ДИБ': StateCategory.TODO,
        'Аналитика': StateCategory.IN_PROGRESS,
        'Готово к разработке': StateCategory.IN_PROGRESS,
        'Разработка': StateCategory.IN_PROGRESS,
        'Разработка тест-кейсов': StateCategory.IN_PROGRESS,
        'Готово к тестированию': StateCategory.IN_PROGRESS,
        'Тестирование': StateCategory.IN_PROGRESS,
        'Test тестирование': StateCategory.IN_PROGRESS,
        'В работе': StateCategory.IN_PROGRESS,
        'Опытно-промышленная эксплуатация': StateCategory.IN_PROGRESS,
        'Code review': StateCategory.IN_PROGRESS,
        'Preprod тестирование': StateCategory.IN_PROGRESS,
        'Готова к переносу на ПРОД': StateCategory.IN_PROGRESS,
        'Выполнена': StateCategory.DONE,
        'Закрыто': StateCategory.DONE,
        'Завершена': StateCategory.DONE,
        'Отменено': StateCategory.DONE,
        'Отложено': StateCategory.DONE,
        'Не согласовано ДИБ': StateCategory.DONE
    }

    states['category_id'] = states['name'].apply(
        lambda state_name: STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING[state_name] if state_name in STATE_NAME_TO_STATE_CATEGORY_ID_MAPPING else StateCategory.NOT_SET
    )
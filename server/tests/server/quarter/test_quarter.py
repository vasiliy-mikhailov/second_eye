import datetime

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.test_data_creator.states_creator import StatesCreator
from second_eye_api.migrate_from_external_db.transform import utils
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill

def test_quarters_loaded():
    creator = test_data_creator.TestDataCreator()
    today = datetime.date.today()
    current_year = today.year
    quarter_key = utils.get_quarter_key(date=today)
    quarter_number = utils.get_quarter_number(date=today)
    quarter_id = creator.create_quarter(name=quarter_key, year=current_year, quarter_number=quarter_number)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    quarters {
        id
        key
        name
    }
}
"""
)
    assert executed == {
        "data": {
            "quarters": [
                { "id": -1, "key": "-1", "name": "Не указано" },
                { "id": quarter_id, "key": quarter_key, "name": quarter_key },
            ]
        }
    }

def test_when_quarter_has_change_request_and_incident_both_are_summed_up():
    creator = test_data_creator.TestDataCreator()

    today = datetime.date.today()
    current_year = today.year
    quarter_key = utils.get_quarter_key(date=today)
    quarter_number = utils.get_quarter_number(date=today)
    quarter_id = creator.create_quarter(name=quarter_key, year=current_year, quarter_number=quarter_number)

    first_day_of_current_month = datetime.date(year=today.year, month=today.month, day=1).strftime('%Y-%m-%d')

    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)

    incident_id = creator.create_incident(
        key="I-1",
        name="Инцидент",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=today
    )
    _ = creator.create_incident_time_sheet(
        incident_id=incident_id,
        date=today,
        time_spent=1.0,
        person_key="-1"
    )
    incident_development_task_id = creator.create_incident_sub_task(key="IDT-1", name="Разработка по инциденту",
                                                                    incident_id=incident_id,
                                                                    skill_id=skill.Skill.DEVELOPMENT)
    _ = creator.create_incident_sub_task_time_sheet(
        incident_sub_task_id=incident_development_task_id,
        date=today,
        time_spent=0.5,
        person_key="-1"
    )

    change_request_id = creator.create_change_request(
        key="CR-1", name="Заявка на доработку кредитного процесса",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=today,
        quarter_key=quarter_key,
    )
    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка на доработку Кредитного конвейера",
        change_request_id=change_request_id,
        system_id=system_id
    )
    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request_id,
        date=today,
        time_spent=5.0,
        person_key="-1"
    )
    analysis_task_id = creator.create_task(
        key="AT-1",
        name="Задача на аналитику Кредитного конвейера",
        system_change_request_id=system_change_request_id,
        skill_id=skill.Skill.ANALYSIS
    )
    development_task_id = creator.create_task(
        key="DT-1",
        name="Задача на разработку Кредитного конвейера",
        system_change_request_id=system_change_request_id,
        skill_id=skill.Skill.DEVELOPMENT
    )
    testing_task_id = creator.create_task(
        key="TT-1",
        name="Задача на тестирование Кредитного конвейера",
        system_change_request_id=system_change_request_id,
        skill_id=skill.Skill.TESTING
    )
    _ = creator.create_task_time_sheet(
        task_id=analysis_task_id,
        date=today,
        time_spent=2.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_id,
        date=today,
        time_spent=3.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_id,
        date=today,
        time_spent=4.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query QuarterByKey($key: String) {
                quarterByKey(key: $key) {
                    id
                    key
                    analysisTimeSpent
                    developmentTimeSpent
                    estimate
                    testingTimeSpent
                    managementTimeSpent
                    incidentFixingTimeSpent
                    timeSpent
                }
            }
        """,
        variables={"key": quarter_key},
    )
    assert executed == {
        "data": {
            "quarterByKey": {
                "id": quarter_id,
                "key": quarter_key,
                "analysisTimeSpent": 2.0,
                "developmentTimeSpent": 3.0,
                "estimate": 15.5,
                "testingTimeSpent": 4.0,
                "managementTimeSpent": 5.0,
                "incidentFixingTimeSpent": 1.5,
                "timeSpent": 15.5,
            }
        }
    }

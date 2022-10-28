import datetime

from server.wsgi import * # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill

def test_companies_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    companies {
        id
        name
    }
}
"""
)
    assert executed == {
        "data": {
            "companies": [
                { "id": -1, "name": "Не указано" },
                { "id": company_id, "name": "Банк" },
            ]
        }
    }


def test_dedicated_teams_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    dedicatedTeams {
        id
        name
        company {
            id
        }
    }
}
"""
)
    assert executed == {
        "data": {
            "dedicatedTeams": [
                { "id": -1, "name": "Не указано", "company": { "id": -1} },
                { "id": dedicated_team_id, "name": "Корпоративный блок", "company": {"id": company_id}},
            ]
        }
    }

def test_systems_loaded():
    creator = test_data_creator.TestDataCreator()
    system_id = creator.create_system(name="Кредитный конвейер")

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    systems {
        id
        name
    }
}
"""
)
    assert executed == {
        "data": {
            "systems": [
                { "id": -1, "name": "Не указано" },
                {"id": system_id, "name": "Кредитный конвейер"},
            ]
        }
    }

def test_epics_loaded():
    creator = test_data_creator.TestDataCreator()
    epic_id = creator.create_epic(key="E-1", name="Модернизация корпоративного кредитного процесса")

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    epics {
        id
        key
        name
    }
}
"""
)
    assert executed == {
        "data": {
            "epics": [
                { "id": -1, "key": "-1", "name": "Не указано" },
                { "id": epic_id, "key": "E-1", "name": "Модернизация корпоративного кредитного процесса" },
            ]
        }
    }

def test_quarters_loaded():
    creator = test_data_creator.TestDataCreator()
    creator.create_planning_period(id=2022)
    quarter_id = creator.create_quarter(name="2022-III", year=2022, quarter_number=3)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    quarters {
        id
        key
        name
        
        start
        end
        
        planningPeriod {
            id
        }
    }
}
"""
)
    assert executed == {
        "data": {
            "quarters": [
                { "id": -1, "key": "-1", "name": "Не указано", "start": str(datetime.date.today()), "end": str(datetime.date.today()), "planningPeriod": {"id": -1 } },
                { "id": quarter_id, "key": "2022-III", "name": "2022-III", "start": "2022-07-01", "end": "2022-09-30", "planningPeriod": { "id": 2022 } },
            ]
        }
    }

def test_change_requests_loaded():
    creator = test_data_creator.TestDataCreator()
    change_request_id = creator.create_change_request(key="CR-1", name="Заявка на доработку кредитного процесса")

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        {
            changeRequests {
                id
                key
                name
            }
        }
        """
    )
    assert executed == {
        "data": {
            "changeRequests": [
                { "id": -1, "key": "-1", "name": "Не указано" },
                { "id": change_request_id, "key": "CR-1", "name": "Заявка на доработку кредитного процесса" },
            ]
        }
    }

def test_system_change_requests_loaded():
    creator = test_data_creator.TestDataCreator()
    change_request_id = creator.create_change_request(key="CR-1", name="Заявка на доработку кредитного процесса")
    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(key="SCR-1", name="Заявка на доработку Кредитного конвейера", change_request_id=change_request_id, system_id=system_id)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        {
            systemChangeRequests {
                id
                key
                name
                
                changeRequest {
                    id
                }
                
                system {
                    id
                }
            }
        }
        """
    )
    assert executed == {
        "data": {
            "systemChangeRequests": [
                { "id": -1, "key": "-1", "name": "Не указано", "changeRequest": { "id": -1 }, "system": { "id": -1} },
                { "id": system_change_request_id, "key": "SCR-1", "name": "Заявка на доработку Кредитного конвейера", "changeRequest": { "id": change_request_id }, "system": { "id": system_id} },
            ]
        }
    }


def test_tasks_loaded():
    creator = test_data_creator.TestDataCreator()
    change_request_id = creator.create_change_request(key="CR-1", name="Заявка на доработку кредитного процесса")
    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка на доработку Кредитного конвейера",
        change_request_id=change_request_id,
        system_id=system_id
    )
    task_id = creator.create_task(
        key="DT-1",
        name="Задача на разработку Кредитного конвейера",
        system_change_request_id=system_change_request_id,
        skill_id=skill.Skill.DEVELOPMENT
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        {
            tasks {
                id
                key
                name
                
                skill {
                    id
                }

                systemChangeRequest {
                    id
                }
            }
        }
        """
    )
    assert executed == {
        "data": {
            "tasks": [
                { "id": -1, "key": "-1", "name": "Не указано", "systemChangeRequest": {"id": -1}, "skill": {"id": -1} },
                { "id": task_id, "key": "DT-1", "name": "Задача на разработку Кредитного конвейера", "systemChangeRequest": {"id": system_change_request_id}, "skill": {"id": skill.Skill.DEVELOPMENT} },
            ]
        }
    }


def test_task_time_sheets_loaded():
    creator = test_data_creator.TestDataCreator()
    change_request_id = creator.create_change_request(key="CR-1", name="Заявка на доработку кредитного процесса")
    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка на доработку Кредитного конвейера",
        change_request_id=change_request_id,
        system_id=system_id
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
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_id,
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_id,
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query SystemChangeRequestByKey($key: String) {
                systemChangeRequestByKey(key: $key) {
                    id
                    timeSpent
                }
            }
        """,
        variables={ "key" : "SCR-1" },
    )
    assert executed == {
        "data": {
            "systemChangeRequestByKey": { "id": system_change_request_id, "timeSpent": 24.0, }
        }
    }
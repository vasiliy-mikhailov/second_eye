import datetime

from server.wsgi import * # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill

def test_incidents_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)
    incident_id = creator.create_incident(key="I-1", name="Инцидент", project_team_id=project_team_id)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
"""
{
    incidents {
        id
        key
        name
        
        projectTeam {
            id
        }
    }
}
"""
)
    assert executed == {
        "data": {
            "incidents": [
                { "id": -1, "key": "-1", "name": "Не указано", "projectTeam": { "id": -1 } },
                { "id": incident_id, "key": "I-1", "name": "Инцидент", "projectTeam": { "id": project_team_id } },
            ]
        }
    }

def test_incident_sub_tasks_loaded():
    creator = test_data_creator.TestDataCreator()
    incident_id = creator.create_incident(key="I-1", name="Инцидент")
    incident_development_task_id = creator.create_incident_sub_task(key="IDT-1", name="Разработка по инциденту", incident_id=incident_id, skill_id=skill.Skill.DEVELOPMENT)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query IncidentSubTaskByKey($key: String) {
                incidentSubTaskByKey(key: $key) {
                    id
                    key
                    name
                    
                    incident {
                        id
                    }
                }
            }
        """,
        variables={ "key" : "IDT-1" },
    )

    assert executed == {
        "data": {
            "incidentSubTaskByKey": { "id": incident_development_task_id, "key": "IDT-1", "name": "Разработка по инциденту", "incident": { "id": incident_id } },
        }
    }


def test_incident_time_sheets_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)
    incident_id = creator.create_incident(key="I-1", name="Инцидент", project_team_id=project_team_id)
    _ = creator.create_incident_time_sheet(
        incident_id=incident_id,
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query IncidentByKey($key: String) {
                incidentByKey(key: $key) {
                    id
                    timeSpent
                }
            }
        """,
        variables={"key": "I-1"},
    )

    assert executed == {
        "data": {
            "incidentByKey": { "id": incident_id, "timeSpent": 8.0 },
        }
    }

def test_incident_sub_task_time_sheets_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)
    incident_id = creator.create_incident(key="I-1", name="Инцидент", project_team_id=project_team_id)
    incident_development_task_id = creator.create_incident_sub_task(key="IDT-1", name="Разработка по инциденту", incident_id=incident_id, skill_id=skill.Skill.DEVELOPMENT)
    _ = creator.create_incident_sub_task_time_sheet(
        incident_sub_task_id=incident_development_task_id,
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query IncidentByKey($key: String) {
                incidentByKey(key: $key) {
                    id
                    timeSpent
                }
            }
        """,
        variables={"key": "I-1"},
    )

    assert executed == {
        "data": {
            "incidentByKey": { "id": incident_id, "timeSpent": 8.0 },
        }
    }

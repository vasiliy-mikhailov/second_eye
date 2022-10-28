import datetime

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from django.conf import settings


def test_non_project_activities_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    non_project_activity_id = creator.create_non_project_activity(key="NPA-1", name="Непроектная деятельность",
                                                                  company_id=company_id)

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        {
            nonProjectActivities {
                id
                key
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
            "nonProjectActivities": [
                {"id": -1, "key": "-1", "name": "Не указано", "company": {"id": -1}},
                {"id": non_project_activity_id, "key": "NPA-1", "name": "Непроектная деятельность",
                 "company": {"id": company_id}},
            ]
        }
    }

def test_non_project_activity_time_sheets_loaded():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    non_project_activity_id = creator.create_non_project_activity(key="NPA-1", name="Непроектная деятельность",
                                                                  company_id=company_id)

    _ = creator.create_non_project_activity_time_sheet(
        non_project_activity_id=non_project_activity_id,
        date=datetime.date.today(),
        time_spent=8.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)

    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query NonProjectActivityByKey($key: String) {
                nonProjectActivityByKey(key: $key) {
                    id
                    timeSpent
                }
            }
        """,
        variables={"key": "NPA-1"},
    )

    assert executed == {
        "data": {
            "nonProjectActivityByKey": { "id": non_project_activity_id, "timeSpent": 8.0 },
        }
    }

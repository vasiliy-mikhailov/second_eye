import datetime
import pytest

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill


def test_when_project_managers_have_change_request_and_incident_both_are_summed_up():
    today = datetime.date.today()
    two_weeks = datetime.timedelta(days=14)
    two_weeks_ago = today - two_weeks
    current_year = today.year

    creator = test_data_creator.TestDataCreator()
    creator.create_planning_period(id=current_year)
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_manager_id, project_manager_key = creator.create_person(name="Руководитель проекта")
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id,
                                                  project_manager_key=project_manager_key)

    incident_id = creator.create_incident(key="I-1", name="Инцидент", project_team_id=project_team_id)
    _ = creator.create_incident_time_sheet(
        incident_id=incident_id,
        date=two_weeks_ago,
        time_spent=1.0,
        person_key="-1"
    )
    incident_development_task_id = creator.create_incident_sub_task(key="IDT-1", name="Разработка по инциденту",
                                                                    incident_id=incident_id,
                                                                    skill_id=skill.Skill.DEVELOPMENT)
    _ = creator.create_incident_sub_task_time_sheet(
        incident_sub_task_id=incident_development_task_id,
        date=two_weeks_ago,
        time_spent=0.5,
        person_key="-1"
    )

    change_request_id = creator.create_change_request(key="CR-1", name="Заявка на доработку кредитного процесса",
                                                      project_team_id=project_team_id)
    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка на доработку Кредитного конвейера",
        change_request_id=change_request_id,
        system_id=system_id
    )
    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request_id,
        date=two_weeks_ago,
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
        date=two_weeks_ago,
        time_spent=2.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_id,
        date=two_weeks_ago,
        time_spent=3.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_id,
        date=two_weeks_ago,
        time_spent=4.0,
        person_key="-1"
    )

    non_project_activity_id = creator.create_non_project_activity(key="NPA-1", name="Непроектная деятельность",
                                                                  company_id=company_id)

    _ = creator.create_non_project_activity_time_sheet(
        non_project_activity_id=non_project_activity_id,
        date=two_weeks_ago,
        time_spent=6.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query ProjectManagers {
                projectManagers {
                    id
                    
                    name
                    
                    isActive
                    
                    analysisTimeSpentChrononFte
                    developmentTimeSpentChrononFte
                    testingTimeSpentChrononFte
                    managementTimeSpentChrononFte
                    incidentFixingTimeSpentChrononFte
                    nonProjectActivityTimeSpentChrononFte
                    
                    timeSpentChrononFte
                }
            }
        """,
        variables={},
    )
    assert executed == {
        "data": {
            "projectManagers": [{
                "id": -1,
                "name": "Не указано",
                "isActive": 0,
                "analysisTimeSpentChrononFte": 0.0,
                "developmentTimeSpentChrononFte": 0.0,
                "testingTimeSpentChrononFte": 0.0,
                "managementTimeSpentChrononFte": 0.0,
                "incidentFixingTimeSpentChrononFte": 0.0,
                "nonProjectActivityTimeSpentChrononFte": pytest.approx(6.0 / 20.0 / 8.0),
                "timeSpentChrononFte": pytest.approx(6.0 / 20.0 / 8.0),
            }, {
                "id": project_manager_id,
                "name": "Руководитель проекта",
                "isActive": 1,
                "analysisTimeSpentChrononFte": 2.0 / 20.0 / 8.0,
                "developmentTimeSpentChrononFte": 3.0 / 20.0 / 8.0,
                "testingTimeSpentChrononFte": 4.0 / 20.0 / 8.0,
                "managementTimeSpentChrononFte": 5.0 / 20.0 / 8.0,
                "incidentFixingTimeSpentChrononFte": pytest.approx(1.5 / 20.0 / 8.0),
                "nonProjectActivityTimeSpentChrononFte": 0.0,
                "timeSpentChrononFte": 15.5 / 20.0 / 8.0,
            }]
        }
    }


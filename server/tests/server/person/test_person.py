import datetime

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.transform import utils
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill

def test_persons_loaded():
    creator = test_data_creator.TestDataCreator()
    person_id, person_key = creator.create_person(name="Исполнитель")

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        {
            persons {
                id
                key
                name
            }
        }
        """
    )
    assert executed == {
        "data": {
            "persons": [
                {"id": -1, "key": "-1", "name": "Не указано"},
                {"id": person_id, "key": person_key, "name": "Исполнитель"},
            ]
        }
    }

def test_when_person_has_change_request_incident_and_non_project_activity_all_are_summed_up():
    creator = test_data_creator.TestDataCreator()
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)

    today = datetime.date.today()
    today_minus_10_working_days = utils.subtract_working_days(from_date=today, number_of_working_days=10)

    person_id, person_key = creator.create_person(name="Исполнитель")

    incident_id = creator.create_incident(key="I-1", name="Инцидент", project_team_id=project_team_id)
    _ = creator.create_incident_time_sheet(
        incident_id=incident_id,
        date=today_minus_10_working_days,
        time_spent=1.0,
        person_key=person_key
    )
    incident_development_task_id = creator.create_incident_sub_task(
        key="IDT-1", name="Разработка по инциденту",
        incident_id=incident_id,
        skill_id=skill.Skill.DEVELOPMENT
    )

    _ = creator.create_incident_sub_task_time_sheet(
        incident_sub_task_id=incident_development_task_id,
        date=today_minus_10_working_days,
        time_spent=0.5,
        person_key=person_key
    )

    change_request_id = creator.create_change_request(
        key="CR-1",
        name="Заявка на доработку кредитного процесса",
        project_team_id=project_team_id
    )

    system_id = creator.create_system(name="Кредитный конвейер")
    system_change_request_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка на доработку Кредитного конвейера",
        change_request_id=change_request_id,
        system_id=system_id,
    )
    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request_id,
        date=today_minus_10_working_days,
        time_spent=5.0,
        person_key=person_key
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
        date=today_minus_10_working_days,
        time_spent=2.0,
        person_key=person_key
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_id,
        date=today_minus_10_working_days,
        time_spent=3.0,
        person_key=person_key
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_id,
        date=today_minus_10_working_days,
        time_spent=4.0,
        person_key=person_key
    )

    non_project_activity_id = creator.create_non_project_activity(key="NPA-1", name="Непроектная деятельность",
                                                                  company_id=company_id)

    _ = creator.create_non_project_activity_time_sheet(
        non_project_activity_id=non_project_activity_id,
        date=today_minus_10_working_days,
        time_spent=6.0,
        person_key=person_key
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query PersonByKey($key: String) {
                personByKey(key: $key) {
                    id
                    key
                    name
                    
                    analysisTimeSpentChronon
                    developmentTimeSpentChronon
                    testingTimeSpentChronon
                    managementTimeSpentChronon
                    incidentFixingTimeSpentChronon
                    nonProjectActivityTimeSpentChronon
                    timeSpentChronon
                    
                    changeRequests {
                        changeRequest {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    dedicatedTeams {
                        dedicatedTeam {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    incidents {
                        incident {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    nonProjectActivities {
                        nonProjectActivity {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    projectTeams {
                        projectTeam {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    projectTeamPositionPersons {
                        projectTeam {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    systemChangeRequests {
                        systemChangeRequest {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                    
                    tasks {
                        task {
                            id
                            name
                        }
                        
                        analysisTimeSpentChronon
                        developmentTimeSpentChronon
                        testingTimeSpentChronon
                        managementTimeSpentChronon
                        incidentFixingTimeSpentChronon
                        nonProjectActivityTimeSpentChronon
                        timeSpentChronon
                    }
                }
            }
        """,
        variables={"key": person_key},
    )
    assert executed == {
        "data": {
            "personByKey": {
                "id": person_id,
                "key": person_key,
                "name": "Исполнитель",
                "analysisTimeSpentChronon": 2.0,
                "developmentTimeSpentChronon": 3.0,
                "testingTimeSpentChronon": 4.0,
                "managementTimeSpentChronon": 5.0,
                "incidentFixingTimeSpentChronon": 1.5,
                "nonProjectActivityTimeSpentChronon": 6.0,
                "timeSpentChronon": 21.5,
                "changeRequests": [
                    {
                        "changeRequest": {
                            "id": change_request_id,
                            "name": "Заявка на доработку кредитного процесса",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 5.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 14.0,
                    },
                ],
                "dedicatedTeams": [
                    {
                        "dedicatedTeam": {
                            "id": -1,
                            "name": "Не указано",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 6.0,
                        "timeSpentChronon": 6.0,
                    },
                    {
                        "dedicatedTeam": {
                            "id": dedicated_team_id,
                            "name": "Корпоративный блок",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 5.0,
                        "incidentFixingTimeSpentChronon": 1.5,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 15.5,
                    },
                ],
                "incidents": [
                    {
                        "incident": {
                            "id": incident_id,
                            "name": "Инцидент",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 1.5,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 1.5,
                    },
                ],
                "nonProjectActivities": [
                    {
                        "nonProjectActivity": {
                            "id": non_project_activity_id,
                            "name": "Непроектная деятельность",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 6.0,
                        "timeSpentChronon": 6.0,
                    },
                ],
                "projectTeams": [
                    {
                        "projectTeam": {
                            "id": -1,
                            "name": "Не указано",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 6.0,
                        "timeSpentChronon": 6.0,
                    },
                    {
                        "projectTeam": {
                            "id": project_team_id,
                            "name": "Корпоративные кредиты",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 5.0,
                        "incidentFixingTimeSpentChronon": 1.5,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 15.5,
                    },
                ],
                "projectTeamPositionPersons": [
                    {
                        "projectTeam": {
                            "id": -1,
                            "name": "Не указано",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 6.0,
                        "timeSpentChronon": 6.0,
                    },
                    {
                        "projectTeam": {
                            "id": project_team_id,
                            "name": "Корпоративные кредиты",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 5.0,
                        "incidentFixingTimeSpentChronon": 1.5,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 15.5,
                    },
                ],
                "systemChangeRequests": [
                    {
                        "systemChangeRequest": {
                            "id": system_change_request_id,
                            "name": "Заявка на доработку Кредитного конвейера",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 5.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 14.0,
                    },
                ],
                "tasks": [
                    {
                        "task": {
                            "id": analysis_task_id,
                            "name": "Задача на аналитику Кредитного конвейера",
                        },
                        "analysisTimeSpentChronon": 2.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 2.0,
                    },
                    {
                        "task": {
                            "id": development_task_id,
                            "name": "Задача на разработку Кредитного конвейера",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 3.0,
                        "testingTimeSpentChronon": 0.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 3.0,
                    },
                    {
                        "task": {
                            "id": testing_task_id,
                            "name": "Задача на тестирование Кредитного конвейера",
                        },
                        "analysisTimeSpentChronon": 0.0,
                        "developmentTimeSpentChronon": 0.0,
                        "testingTimeSpentChronon": 4.0,
                        "managementTimeSpentChronon": 0.0,
                        "incidentFixingTimeSpentChronon": 0.0,
                        "nonProjectActivityTimeSpentChronon": 0.0,
                        "timeSpentChronon": 4.0,
                    },
                ],
            },
        }
    }



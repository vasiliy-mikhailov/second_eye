import datetime
import pytest

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill
from second_eye_api.migrate_from_external_db.transform import utils


def test_change_request_detail():
    today = datetime.date.today()
    two_weeks = datetime.timedelta(days=14)
    two_weeks_ago = today - two_weeks
    two_weeks_ago_string = two_weeks_ago.strftime('%Y-%m-%d')
    first_day_of_month_two_weeks_ago = datetime.date(year=two_weeks_ago.year, month=two_weeks_ago.month,
                                                     day=1).strftime(
        '%Y-%m-%d')
    current_year = today.year
    working_days_in_month_occured = utils.working_days_in_month_occured(for_date=two_weeks_ago, sys_date=today)

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
            query ChangeRequestByKeyQuery($key: String!) {
                changeRequestByKey(key: $key) {
                    id 
                    key
                    url
                    name
                    state {
                        name
                    }
                    
                    analysisEstimate
                    analysisTimeSpent
                    analysisTimeLeft
                    analysisTimeSheetsByDate {
                        date
                        timeSpentCumsum
                    }
                    
                    developmentEstimate
                    developmentTimeSpent
                    developmentTimeLeft
                    developmentTimeSheetsByDate {
                        date
                        timeSpentCumsum
                    }
                    
                    testingEstimate
                    testingTimeSpent
                    testingTimeLeft
                    testingTimeSheetsByDate {
                        date
                        timeSpentCumsum
                    }
                    
                    estimate
                    effortPerFunctionPoint
                    timeSpent
                    timeLeft
                    timeSheetsByDate {
                        date
                        timeSpentCumsum
                        timeSpentCumsumPrediction
                    }
                    
                    plannedInstallDate
                    
                    calculatedFinishDate
                    
                    systemChangeRequests {
                        id
                        key
                        name
                        
                        estimate
                        effortPerFunctionPoint
                        
                        timeLeft
                        state {
                            name
                        }
                        stateCategory {
                            id
                        }
                        
                        calculatedFinishDate
                        
                        mainDeveloper {
                            id
                            name
                        }
                    }
                    
                    persons {
                        person {
                            id
                            name
                        }
                        timeSpent
                        timeSpentChrononFte
                    }
                }
            }
        """,
        variables={"key": "CR-1"},
    )
    assert executed == {
        "data": {
            "changeRequestByKey": {
                "id": change_request_id,
                "key": "CR-1",
                "url": "",
                "name": "Заявка на доработку кредитного процесса",
                "state": {
                    "name": "Не указано"
                },
                "analysisEstimate": 2.0,
                "analysisTimeSpent": 2.0,
                "analysisTimeLeft": 0.0,
                "analysisTimeSheetsByDate": [{
                    "date": two_weeks_ago_string,
                    "timeSpentCumsum": 2.0,
                }],
                "developmentEstimate": 3.0,
                "developmentTimeSpent": 3.0,
                "developmentTimeLeft": 0.0,
                "developmentTimeSheetsByDate": [{
                    "date": two_weeks_ago_string,
                    "timeSpentCumsum": 3.0,
                }],
                "testingEstimate": 4.0,
                "testingTimeSpent": 4.0,
                "testingTimeLeft": 0.0,
                "testingTimeSheetsByDate": [{
                    "date": two_weeks_ago_string,
                    "timeSpentCumsum": 4.0,
                }],
                "estimate": 14.0,
                "effortPerFunctionPoint": 0.0,
                "timeSpent": 14.0,
                "timeLeft": 0.0,
                "timeSheetsByDate": [{
                    "date": two_weeks_ago_string,
                    "timeSpentCumsum": 14.0,
                    "timeSpentCumsumPrediction": 0.0,
                }],
                "plannedInstallDate": None,
                "calculatedFinishDate": two_weeks_ago_string,
                "systemChangeRequests": [{
                    "id": system_change_request_id,
                    "key": "SCR-1",
                    "name": "Заявка на доработку Кредитного конвейера",
                    "estimate": 14.0,
                    "effortPerFunctionPoint": 0.0,
                    "timeLeft": 0.0,
                    "state": {
                        "name": "Не указано",
                    },
                    "stateCategory": {
                        "id": -1,
                    },
                    "calculatedFinishDate": two_weeks_ago_string,
                    "mainDeveloper": {
                        "id": -1,
                        "name": "Не указано"
                    },
                }],
                "persons": [{
                    "person": {
                        "id": -1,
                        "name": "Не указано"
                    },
                    "timeSpent": 14.0,
                    "timeSpentChrononFte": pytest.approx(14.0 / 20.0 / 8.0),
                }]
            }
        }
    }

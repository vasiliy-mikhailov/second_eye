import datetime
import pytest

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.test_data_creator.states_creator import StatesCreator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill
from second_eye_api.migrate_from_external_db.transform import utils
from tests.utils import AnyValue

def test_dedicated_team_planning_period():
    creator = test_data_creator.TestDataCreator()

    today = datetime.date.today()
    today_minus_10_working_days = utils.subtract_working_days(from_date=today, number_of_working_days=10)
    today_minus_10_working_days_string = today_minus_10_working_days.strftime('%Y-%m-%d')
    current_year = today.year
    current_year_string = str(current_year)
    first_day_of_current_year = datetime.date(year=today.year, month=1, day=1)
    first_day_of_current_year_string = first_day_of_current_year.strftime('%Y-%m-%d')
    last_day_of_current_year = datetime.date(year=today.year, month=12, day=31)
    last_day_of_current_year_string = last_day_of_current_year.strftime('%Y-%m-%d')

    creator.create_planning_period(id=current_year)
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
        date=today_minus_10_working_days,
        time_spent=1.0,
        person_key="-1"
    )
    incident_development_task_id = creator.create_incident_sub_task(key="IDT-1", name="Разработка по инциденту",
                                                                    incident_id=incident_id,
                                                                    skill_id=skill.Skill.DEVELOPMENT)
    _ = creator.create_incident_sub_task_time_sheet(
        incident_sub_task_id=incident_development_task_id,
        date=today_minus_10_working_days,
        time_spent=0.5,
        person_key="-1"
    )

    change_request_id = creator.create_change_request(
        key="CR-1", name="Заявка на доработку кредитного процесса",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=today
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
        date=today_minus_10_working_days,
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
        date=today_minus_10_working_days,
        time_spent=2.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_id,
        date=today_minus_10_working_days,
        time_spent=3.0,
        person_key="-1"
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_id,
        date=today_minus_10_working_days,
        time_spent=4.0,
        person_key="-1"
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
        query DedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId($planningPeriodId: Int!, $dedicatedTeamId: Int!) {
              dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId(dedicatedTeamId: $dedicatedTeamId, planningPeriodId: $planningPeriodId) {
                    #id
                    estimate
                    effortPerFunctionPoint
                    calculatedFinishDate
                    dedicatedTeam {
                        name
                        cio {
                            name
                        }
                        cto {
                            name
                        }
                    }
                    planningPeriod {
                        name
                        start
                        end
                    }
                    timeSheetsByDate {
                        date
                        timeSpentCumsum
                        timeSpentCumsumPrediction
                        timeSpentWithoutValuePercentCumsum
                        timeSpentWithValuePercentCumsum
                        timeSpentForReengineeringPercentCumsum
                        timeSpentNotForReengineeringPercentCumsum
                    }
                    
                    projectTeamPlanningPeriods {
                        id
                        estimate
                        timeLeft
                        projectTeam {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                        timeSpentChronon
                    }
                    
                    dedicatedTeamPlanningPeriodSystems {
                        id
                        estimate
                        timeLeft
                        system {
                            id
                            name
                        }
                        effortPerFunctionPoint
                        calculatedFinishDate
                    }
                    
                    changeRequests {
                        id
                        key
                        estimate
                        timeLeft
                        hasValue
                        name
                        stateCategoryId
                        effortPerFunctionPoint
                        calculatedFinishDate
                        timeSpentChronon
                    }
                    
                    positionPersons {
                        position {
                            id
                            name
                            url
                        }
                        
                        person {
                            id
                            key
                            name
                        }
                        timeSpent
                        timeSpentChrononFte
                        totalCapacityFte
                    }
              }
        }
        """,
        variables={"planningPeriodId": current_year, "dedicatedTeamId": dedicated_team_id},
    )
    assert executed == {
        "data": {
            "dedicatedTeamPlanningPeriodByPlanningPeriodIdAndDedicatedTeamId": {
                "estimate": 15.5,
                "effortPerFunctionPoint": 0.0,
                "calculatedFinishDate": today_minus_10_working_days_string,
                "dedicatedTeam": {
                    "name": "Корпоративный блок",
                    "cio": {
                        "name": "Не указано",
                    },
                    "cto": {
                        "name": "Не указано",
                    },
                },
                "planningPeriod": {
                    "name": current_year_string,
                    "start": first_day_of_current_year_string,
                    "end": last_day_of_current_year_string,
                },
                "timeSheetsByDate": [{
                    "date": today_minus_10_working_days_string,
                    "timeSpentCumsum": 15.5,
                    "timeSpentCumsumPrediction": 0.0,
                    "timeSpentWithoutValuePercentCumsum": pytest.approx(1 - 1.5 / 15.5),
                    "timeSpentWithValuePercentCumsum": pytest.approx(1.5 / 15.5),
                    "timeSpentForReengineeringPercentCumsum": pytest.approx(1.5 / 15.5),
                    "timeSpentNotForReengineeringPercentCumsum": pytest.approx(1 - 1.5 / 15.5),
                }],
                "projectTeamPlanningPeriods": [{
                    "id": AnyValue(),
                    "estimate": 15.5,
                    "timeLeft": 0.0,
                    "projectTeam": {
                        "id": project_team_id,
                        "name": "Корпоративные кредиты",
                    },
                    "effortPerFunctionPoint": 0.0,
                    "calculatedFinishDate": today_minus_10_working_days_string,
                    "timeSpentChronon": 15.5,
                }],
                "dedicatedTeamPlanningPeriodSystems": [{
                    "id": AnyValue(),
                    "estimate": 14.0,
                    "timeLeft": 0.0,
                    "system": {
                        "id": system_id,
                        "name": "Кредитный конвейер",
                    },
                    "effortPerFunctionPoint": 0.0,
                    "calculatedFinishDate": today_minus_10_working_days_string,
                }],
                "changeRequests": [{
                    "id": change_request_id,
                    "key": "CR-1",
                    "estimate": 14.0,
                    "timeLeft": 0.0,
                    "hasValue": False,
                    "name": "Заявка на доработку кредитного процесса",
                    "stateCategoryId": 3,
                    "effortPerFunctionPoint": 0.0,
                    "calculatedFinishDate": today_minus_10_working_days_string,
                    "timeSpentChronon": 14.0,
                }],
                "positionPersons": [{
                    "position": {
                        "id": -1,
                        "name": "Не указано",
                        "url": "",
                    },
                    "person": {
                        "id": -1,
                        "key": "-1",
                        "name": "Не указано",
                    },
                    "timeSpent": 15.5,
                    "timeSpentChrononFte": pytest.approx(15.5 / 20.0 / 8.0),
                    "totalCapacityFte": 0.0,
                }],
            }
        }
    }


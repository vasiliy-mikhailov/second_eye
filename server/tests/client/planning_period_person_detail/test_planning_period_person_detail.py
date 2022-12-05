import datetime
import pytest

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.test_data_creator.states_creator import StatesCreator
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import function_component
from second_eye_api.migrate_from_external_db.transform import skill
from second_eye_api.migrate_from_external_db.transform import utils


def test_planning_period_person_detail():
    today = datetime.date.today()
    two_weeks = datetime.timedelta(days=14)
    two_weeks_ago = today - two_weeks
    two_weeks_ago_string = two_weeks_ago.strftime('%Y-%m-%d')
    first_day_of_month_two_weeks_ago = datetime.date(year=two_weeks_ago.year, month=two_weeks_ago.month,
                                                     day=1).strftime(
        '%Y-%m-%d')
    two_weeks_ago_year = two_weeks_ago.year
    working_days_in_month_occured = utils.working_days_in_month_occured(for_date=two_weeks_ago, sys_date=today)

    creator = test_data_creator.TestDataCreator()
    creator.create_planning_period(id=two_weeks_ago_year)
    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_manager_id, project_manager_key = creator.create_person(name="Руководитель проекта")
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id,
                                                  project_manager_key=project_manager_key)

    person1_id, person1_key = creator.create_person("Исполнитель 1")
    person2_id, person2_key = creator.create_person("Исполнитель 2")
    system_id = creator.create_system(name="Кредитный конвейер")

    change_request1_id = creator.create_change_request(
        key="CR-1",
        name="Заявка №1 на доработку кредитного процесса",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=two_weeks_ago
    )

    system_change_request1_1_id = creator.create_system_change_request(
        key="SCR-1",
        name="Заявка №1.1 на доработку Кредитного конвейера",
        change_request_id=change_request1_id,
        system_id=system_id
    )
    analysis_task_1_1_1_id = creator.create_task(
        key="AT-1",
        name="Задача №1.1.1 на аналитику Кредитного конвейера",
        system_change_request_id=system_change_request1_1_id,
        skill_id=skill.Skill.ANALYSIS
    )
    development_task_1_1_2_id = creator.create_task(
        key="DT-1",
        name="Задача №1.1.2 на разработку Кредитного конвейера",
        system_change_request_id=system_change_request1_1_id,
        skill_id=skill.Skill.DEVELOPMENT
    )
    function_component_1_1_2_1_id = creator.create_function_component(
        task_id=development_task_1_1_2_id,
        kind_id=function_component.FunctionComponentKind.TABLE,
        name="Таблица",
        count=1
    )
    testing_task_1_1_3_id = creator.create_task(
        key="TT-1",
        name="Задача №1.1.3 на тестирование Кредитного конвейера",
        system_change_request_id=system_change_request1_1_id,
        skill_id=skill.Skill.TESTING
    )

    change_request2_id = creator.create_change_request(
        key="CR-2",
        name="Заявка №2 на доработку кредитного процесса",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=two_weeks_ago
    )
    system_change_request2_1_id = creator.create_system_change_request(
        key="SCR-2",
        name="Заявка №2.1 на доработку Кредитного конвейера",
        change_request_id=change_request2_id,
        system_id=system_id
    )
    analysis_task_2_1_1_id = creator.create_task(
        key="AT-2",
        name="Задача №2.1.1 на аналитику Кредитного конвейера",
        system_change_request_id=system_change_request2_1_id,
        skill_id=skill.Skill.ANALYSIS
    )
    development_task_2_1_2_id = creator.create_task(
        key="DT-2",
        name="Задача №2.1.2 на разработку Кредитного конвейера",
        system_change_request_id=system_change_request2_1_id,
        skill_id=skill.Skill.DEVELOPMENT
    )
    function_component_1_1_2_1_id = creator.create_function_component(
        task_id=development_task_2_1_2_id,
        kind_id=function_component.FunctionComponentKind.OUTPUT,
        name="3 отчета",
        count=3
    )
    testing_task_2_1_3_id = creator.create_task(
        key="TT-2",
        name="Задача №1.1.3 на тестирование Кредитного конвейера",
        system_change_request_id=system_change_request2_1_id,
        skill_id=skill.Skill.TESTING
    )

    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request1_1_id,
        date=two_weeks_ago,
        time_spent=1.0,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=analysis_task_1_1_1_id,
        date=two_weeks_ago,
        time_spent=1.5,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_1_1_2_id,
        date=two_weeks_ago,
        time_spent=2.5,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_1_1_2_id,
        date=two_weeks_ago,
        time_spent=10,
        person_key=person2_key
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_1_1_3_id,
        date=two_weeks_ago,
        time_spent=3.0,
        person_key=person1_key
    )

    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request2_1_id,
        date=two_weeks_ago,
        time_spent=0.5,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=analysis_task_2_1_1_id,
        date=two_weeks_ago,
        time_spent=1.0,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=development_task_2_1_2_id,
        date=two_weeks_ago,
        time_spent=2.5,
        person_key=person1_key
    )
    _ = creator.create_task_time_sheet(
        task_id=testing_task_2_1_3_id,
        date=two_weeks_ago,
        time_spent=5.0,
        person_key=person1_key
    )
    _ = creator.create_management_time_sheet(
        system_change_request_id=system_change_request2_1_id,
        date=two_weeks_ago,
        time_spent=6,
        person_key=person2_key
    )

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
            query PlanningPeriodPersonByPlanningPeriodIdAndPersonKeyQuery($planningPeriodId: Int!, $personKey: String!) {
                planningPeriodPersonByPlanningPeriodIdAndPersonKey(planningPeriodId: $planningPeriodId, personKey: $personKey) {
                  systemChangeRequests {
                    systemChangeRequest {
                        id
                        key
                        name
                        effortPerFunctionPoint
                    }
                    functionPointsEffort
                    percentageOfPersonTotalTimeInPlanningPeriod
                    effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod
                  }
                }
            }
        """,
        variables={"personKey": person1_key, "planningPeriodId": two_weeks_ago_year},
    )
    assert executed == {
        "data": {
            "planningPeriodPersonByPlanningPeriodIdAndPersonKey": {
                "systemChangeRequests": [{
                    "systemChangeRequest": {
                        "id": system_change_request1_1_id,
                        "key": "SCR-1",
                        "name": "Заявка №1.1 на доработку Кредитного конвейера",
                        "effortPerFunctionPoint": pytest.approx(15 / 10),
                    },
                    "functionPointsEffort": 5,
                    "percentageOfPersonTotalTimeInPlanningPeriod": pytest.approx(5 / 9),
                    "effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod": pytest.approx(15 / 10 * 5 / 9),
                }, {
                    "systemChangeRequest": {
                        "id": system_change_request2_1_id,
                        "key": "SCR-2",
                        "name": "Заявка №2.1 на доработку Кредитного конвейера",
                        "effortPerFunctionPoint": pytest.approx(10 / 15),
                    },
                    "functionPointsEffort": 4,
                    "percentageOfPersonTotalTimeInPlanningPeriod": pytest.approx(4 / 9),
                    "effortPerFunctionPointWeightedByPersonTotalTimeInPlanningPeriod": pytest.approx(10 / 15 * 4 / 9),
                },],
            }
        }
    }


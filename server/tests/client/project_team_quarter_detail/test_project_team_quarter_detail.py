import datetime
import pytest

from server.wsgi import *  # загрузить django. Без этой строчки будет ошибка improperly configured
from server import schema
from graphene.test import Client
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.test_data_creator.states_creator import StatesCreator
from second_eye_api.migrate_from_external_db.transform import utils
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill
from second_eye_api.migrate_from_external_db.transform import state
from tests.utils import AnyValue


def test_project_team_quarter_detail():
    creator = test_data_creator.TestDataCreator()

    today = datetime.date.today()

    two_weeks = datetime.timedelta(days=14)
    two_weeks_ago = today - two_weeks
    two_weeks_ago_string = two_weeks_ago.strftime('%Y-%m-%d')
    first_day_of_month_two_weeks_ago = datetime.date(year=two_weeks_ago.year, month=two_weeks_ago.month,
                                                     day=1).strftime(
        '%Y-%m-%d')
    two_weeks_ago_year = two_weeks_ago.year
    working_days_in_month_occured = utils.working_days_in_month_occured(for_date=two_weeks_ago, sys_date=today)

    quarter_key = utils.get_quarter_key(date=two_weeks_ago)
    quarter_number = utils.get_quarter_number(date=two_weeks_ago)
    quarter_id = creator.create_quarter(name=quarter_key, year=two_weeks_ago_year, quarter_number=quarter_number)

    quarter_start_date = utils.get_quarter_start_date(date=two_weeks_ago)
    quarter_start_date_string = quarter_start_date.strftime('%Y-%m-%d')

    quarter_end_date = utils.get_quarter_end_date(date=two_weeks_ago)
    quarter_end_date_string = quarter_end_date.strftime('%Y-%m-%d')

    company_id = creator.create_company(name="Банк")
    dedicated_team_id = creator.create_dedicated_team(name="Корпоративный блок", company_id=company_id)
    project_team_id = creator.create_project_team(name="Корпоративные кредиты", dedicated_team_id=dedicated_team_id)

    incident_id = creator.create_incident(
        key="I-1",
        name="Инцидент",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=two_weeks_ago
    )
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

    change_request_id = creator.create_change_request(
        key="CR-1", name="Заявка на доработку кредитного процесса",
        project_team_id=project_team_id,
        state_id=StatesCreator.DONE_ID,
        resolution_date=two_weeks_ago,
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

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=creator)
    graphene_client = Client(schema.schema)

    executed = graphene_client.execute(
        """
           query ProjectTeamQuarterByQuarterKeyAndProjectTeamId($quarterKey: String!, $projectTeamId: Int!) {
                  projectTeamQuarterByQuarterKeyAndProjectTeamId(projectTeamId: $projectTeamId, quarterKey: $quarterKey) {
                        id
                        estimate
                        effortPerFunctionPoint
                        calculatedFinishDate
                        changeRequestCalculatedDateAfterQuarterEndIssueCount
                        changeRequestCount
                        changeRequestCalculatedDateBeforeQuarterEndShare
                        timeSpentInCurrentQuarterForQuarterChangeRequestsShare

                        projectTeam {
                            name

                            changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter {
                                id
                                changeRequest {
                                    id
                                    key
                                    estimate
                                    timeLeft
                                    hasValue
                                    name
                                    stateCategoryId
                                    effortPerFunctionPoint
                                    calculatedFinishDate
                                    timeSpentInCurrentQuarter
                                }
                            }

                            personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter {
                                id
                                person {
                                    id
                                    key
                                    name
                              }
                              timeSpentInCurrentQuarter
                            }
                        }
                        quarter {
                            key
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

                        projectTeamQuarterSystems {
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
                            timeSpentInCurrentQuarter
                        }
                  }
            }
        """,
        variables={"projectTeamId": project_team_id, "quarterKey": quarter_key},
    )
    assert executed == {
        "data": {
            "projectTeamQuarterByQuarterKeyAndProjectTeamId": {
                "id": AnyValue(),
                "estimate": 15.5,
                "effortPerFunctionPoint": 0.0,
                "calculatedFinishDate": two_weeks_ago_string,
                "changeRequestCalculatedDateAfterQuarterEndIssueCount": 0,
                "changeRequestCount": 1,
                "changeRequestCalculatedDateBeforeQuarterEndShare": 1.0,
                "timeSpentInCurrentQuarterForQuarterChangeRequestsShare": 1.0,
                "projectTeam": {
                    "name": "Корпоративные кредиты",
                    "changeRequestsWithTimeSpentInCurrentQuarterWhileItIsNotInCurrentQuarter": [],
                    "personsWithTimeSpentForChangeRequestsInCurrentQuarterWhileChangeRequestNotInCurrentQuarter": []
                },
                "quarter": {
                    "key": quarter_key,
                    "name": quarter_key,
                    "start": quarter_start_date_string,
                    "end": quarter_end_date_string,
                },
                "timeSheetsByDate": [{
                    "date": two_weeks_ago_string,
                    "timeSpentCumsum": 15.5,
                    "timeSpentCumsumPrediction": 0.0,
                    "timeSpentWithoutValuePercentCumsum": pytest.approx(1 - 1.5 / 15.5),
                    "timeSpentWithValuePercentCumsum": pytest.approx(1.5 / 15.5),
                    "timeSpentForReengineeringPercentCumsum": pytest.approx(1.5 / 15.5),
                    "timeSpentNotForReengineeringPercentCumsum": pytest.approx(1 - 1.5 / 15.5),
                }],
                "projectTeamQuarterSystems": [{
                    "id": AnyValue(),
                    "estimate": 14.0,
                    "timeLeft": 0.0,
                    "system": {
                        "id": system_id,
                        "name": "Кредитный конвейер",
                    },
                    "effortPerFunctionPoint": 0.0,
                    "calculatedFinishDate": two_weeks_ago_string,
                }],
                "changeRequests": [{
                    "id": change_request_id,
                    "key": "CR-1",
                    "estimate": 14.0,
                    "timeLeft": 0.0,
                    "hasValue": False,
                    "name": "Заявка на доработку кредитного процесса",
                    "stateCategoryId": state.StateCategory.DONE,
                    "effortPerFunctionPoint": 0.0,
                    "calculatedFinishDate": two_weeks_ago_string,
                    "timeSpentInCurrentQuarter": 14.0,
                }]
            }
        }
    }


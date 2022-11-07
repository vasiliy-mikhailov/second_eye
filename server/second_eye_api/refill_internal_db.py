import datetime
import django.db
import os
from second_eye_api.migrate_from_external_db.migrate import migrate
from threading import Thread
import traceback
import logging
import time
from django.conf import settings
from .migrate_from_external_db.extract import Extractor

from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db import test_data_creator
from second_eye_api.migrate_from_external_db.test_data_creator.states_creator import StatesCreator
from second_eye_api.migrate_from_external_db.transform import utils
from django.conf import settings
from second_eye_api.migrate_from_external_db.transform import skill
from second_eye_api.migrate_from_external_db.transform import state
from tests.utils import AnyValue

def get_connection_to_real_db():
    pool = settings.pool

    connection = pool.acquire()

    return connection

def refill_internal_db_from_real_db_once():
    import cx_Oracle
    dsn = "Jira-db1.mcb.ru/orcl"

    settings.pool = cx_Oracle.SessionPool(
        user='jiraro',
        password='jiraro',
        dsn=dsn,
        encoding='UTF-8',
        min=2,
        max=30,
        increment=1,
        getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
        threaded=True
    )

    get_input_connection = get_connection_to_real_db

    extractor = Extractor(get_connection=get_input_connection)
    settings.GRAPHENE_FRAME_DATA_STORE = migrate(extractor=extractor)

def refill_internal_db_from_real_db_in_cycle():
    while (True):
        try:
            refill_internal_db_from_real_db_once()
        except Exception as e:
            logging.error(traceback.format_exc())
            print(traceback.format_exc())
        finally:
            time.sleep(10)

def refill_internal_db_from_real_db_in_cycle_in_background():
    t = Thread(target=refill_internal_db_from_real_db_in_cycle, daemon=True)
    t.start()

def refill_internal_db_from_demo_db_once():
    creator = test_data_creator.TestDataCreator()

    today = datetime.date.today()
    current_year = today.year
    creator.create_planning_period(id=current_year)

    two_weeks = datetime.timedelta(days=14)
    two_weeks_ago = today - two_weeks
    two_weeks_ago_string = two_weeks_ago.strftime('%Y-%m-%d')
    first_day_of_month_two_weeks_ago = datetime.date(year=two_weeks_ago.year, month=two_weeks_ago.month, day=1).strftime(
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

    company_id = creator.create_company(id=1, name="Банк")
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

def refill_internal_db(is_demo):
    if is_demo:
        refill_internal_db_from_demo_db_once()
    else:
        refill_internal_db_from_real_db_in_cycle_in_background()

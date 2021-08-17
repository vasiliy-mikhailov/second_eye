import django.db
import os
from second_eye_api.migrate_from_external_db.migrate import migrate
from second_eye_api.migrate_from_external_db.settings import Settings
from threading import Thread
import traceback
import logging
import time

def find_database_switching_router():
    switch_databases_method_name = 'switch_databases'

    routers = django.db.router.routers

    for router in routers:
        try:
            _ = getattr(router, switch_databases_method_name)

            return router
        except AttributeError:
            # If the router doesn't have a method, skip to the next one.
            pass

    return None

def get_connection_to_jira_db():
    import cx_Oracle
    dsn = "Jira-db1.mcb.ru/orcl"

    return cx_Oracle.connect(user='jiraro', password='jiraro', dsn=dsn, encoding='UTF-8')

def refill_internal_db():
    get_input_connection = get_connection_to_jira_db
    router = find_database_switching_router()
    output_database = router.database_for_write
    settings = Settings(last_period_number_of_days=14)

    migrate(get_input_connection=get_input_connection, output_database=output_database, settings=settings)

    router.switch_databases()

def refill_internal_db_in_cycle():
    while (True):
        try:
            refill_internal_db()
        except Exception as e:
            logging.error(traceback.format_exc())
            print(traceback.format_exc())
        finally:
            time.sleep(10)

def refill_internal_db_in_cycle_in_background():
    t = Thread(target=refill_internal_db_in_cycle, daemon=True)
    t.start()

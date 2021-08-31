import django.db
import os
from second_eye_api.migrate_from_external_db.migrate import migrate
from threading import Thread
import traceback
import logging
import time
from django.conf import settings

def get_connection_to_jira_db():
    pool = settings.pool

    connection = pool.acquire()

    return connection

def refill_internal_db():
    import cx_Oracle
    dsn = "Jira-db1.mcb.ru/orcl"

    settings.pool = cx_Oracle.SessionPool(
        user='jiraro',
        password='jiraro',
        dsn=dsn,
        encoding='UTF-8',
        min=2,
        max=15,
        increment=1,
        getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
        threaded=True
    )

    get_input_connection = get_connection_to_jira_db

    settings.GRAPHENE_FRAME_DATA_STORE = migrate(get_input_connection=get_input_connection)

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

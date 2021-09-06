from second_eye_api.schema.state_category import StateCategory
import pandas as pd
from second_eye_api.migrate_from_external_db.transform.utils import *

def calculate_change_requests_actual_change_request_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    return calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities=change_requests,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="change_request_id"
    )

def calculate_change_requests_actual_analysis_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    return calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities=change_requests,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="change_request_id"
    )

def calculate_change_requests_actual_development_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    return calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities=change_requests,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="change_request_id"
    )

def calculate_change_requests_actual_testing_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    return calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities=change_requests,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="change_request_id"
    )
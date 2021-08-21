import pandas as pd

from second_eye_api.models import Skill
from second_eye_api.migrate_from_external_db.transform.utils import *

def calculate_companies_time_left_by_tasks_time_left(companies, tasks):
    return calculate_entities_time_left_by_tasks_time_left_summing_up_by_column(
        entities=companies,
        tasks=tasks,
        sum_up_by_column="company_id"
    )

def calculate_companies_actual_change_request_capacity_by_task_time_sheets(companies, task_time_sheets):
    return calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities=companies,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="company_id"
    )

def calculate_companies_queue_length_inplace(companies):
    companies["queue_length"] = companies.apply(lambda x:
        x["time_left"] / x["actual_change_request_capacity"] if x["actual_change_request_capacity"] > 0 else 0,
        axis=1
    )

def calculate_companies_analysis_time_left_by_tasks_time_left(companies, tasks):
    return calculate_entities_analysis_time_left_by_tasks_time_left_summing_up_by_column(
        entities=companies,
        tasks=tasks,
        sum_up_by_column="company_id"
    )

def calculate_companies_actual_analysis_capacity_by_task_time_sheets(companies, task_time_sheets):
    return calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities=companies,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="company_id"
    )

def calculate_companies_analysis_queue_length_inplace(companies):
    companies["analysis_queue_length"] = companies.apply(lambda x:
        x["analysis_time_left"] / x["actual_analysis_capacity"] if x["actual_analysis_capacity"] > 0 else 0,
        axis=1
    )

def calculate_companies_development_time_left_by_tasks_time_left(companies, tasks):
    return calculate_entities_development_time_left_by_tasks_time_left_summing_up_by_column(
        entities=companies,
        tasks=tasks,
        sum_up_by_column="company_id"
    )

def calculate_companies_actual_developmen_capacity_by_task_time_sheets(companies, task_time_sheets):
    return calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities=companies,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="company_id"
    )

def calculate_companies_development_queue_length_inplace(companies):
    companies["development_queue_length"] = companies.apply(lambda x:
        x["development_time_left"] / x["actual_development_capacity"] if x["actual_development_capacity"] > 0 else 0,
        axis=1
    )

def calculate_companies_testing_time_left_by_tasks_time_left(companies, tasks):
    return calculate_entities_testing_time_left_by_tasks_time_left_summing_up_by_column(
        entities=companies,
        tasks=tasks,
        sum_up_by_column="company_id"
    )

def calculate_companies_actual_testing_capacity_by_task_time_sheets(companies, task_time_sheets):
    return calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities=companies,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="company_id"
    )

def calculate_companies_testing_queue_length_inplace(companies):
    companies["testing_queue_length"] = companies.apply(lambda x:
        x["testing_time_left"] / x["actual_testing_capacity"] if x["actual_testing_capacity"] > 0 else 0,
        axis=1
    )
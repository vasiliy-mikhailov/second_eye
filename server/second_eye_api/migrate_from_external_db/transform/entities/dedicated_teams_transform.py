from second_eye_api.migrate_from_external_db.transform.utils import *

def calculate_dedicated_teams_actual_change_request_capacity_by_task_time_sheets(dedicated_teams, task_time_sheets):
    return calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities=dedicated_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="dedicated_team_id"
    )

def calculate_dedicated_teams_queue_length_inplace(dedicated_teams):
    dedicated_teams["queue_length"] = dedicated_teams.apply(lambda x:
        x["time_left"] / x["actual_change_request_capacity"] if x["actual_change_request_capacity"] > 0 else 0,
        axis=1
    )

def calculate_dedicated_teams_actual_analysis_capacity_by_task_time_sheets(dedicated_teams, task_time_sheets):
    return calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities=dedicated_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="dedicated_team_id"
    )

def calculate_dedicated_teams_analysis_queue_length_inplace(dedicated_teams):
    dedicated_teams["analysis_queue_length"] = dedicated_teams.apply(lambda x:
        x["analysis_time_left"] / x["actual_analysis_capacity"] if x["actual_analysis_capacity"] > 0 else 0,
        axis=1
    )

def calculate_dedicated_teams_actual_development_capacity_by_task_time_sheets(dedicated_teams, task_time_sheets):
    return calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities=dedicated_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="dedicated_team_id"
    )

def calculate_dedicated_teams_development_queue_length_inplace(dedicated_teams):
    dedicated_teams["development_queue_length"] = dedicated_teams.apply(lambda x:
        x["development_time_left"] / x["actual_development_capacity"] if x["actual_development_capacity"] > 0 else 0,
        axis=1
    )

def calculate_dedicated_teams_actual_testing_capacity_by_task_time_sheets(dedicated_teams, task_time_sheets):
    return calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities=dedicated_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="dedicated_team_id"
    )

def calculate_dedicated_teams_testing_queue_length_inplace(dedicated_teams):
    dedicated_teams["testing_queue_length"] = dedicated_teams.apply(lambda x:
        x["testing_time_left"] / x["actual_testing_capacity"] if x["actual_testing_capacity"] > 0 else 0,
        axis=1
    )
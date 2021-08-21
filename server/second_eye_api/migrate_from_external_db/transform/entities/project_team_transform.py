from second_eye_api.migrate_from_external_db.transform.utils import *

def propagate_dedicated_teams_company_id_into_project_teams(project_teams, dedicated_teams):
    dedicated_team_id_to_company_id_mapping = dedicated_teams[["id", "company_id"]].rename(
        columns={"id": "dedicated_team_id"})

    return project_teams.merge(
        dedicated_team_id_to_company_id_mapping,
        how="left",
        on="dedicated_team_id",
        suffixes=(None, ""),
    )

def calculate_project_teams_time_left_by_tasks_time_left(project_teams, tasks):
    return calculate_entities_time_left_by_tasks_time_left_summing_up_by_column(
        entities=project_teams,
        tasks=tasks,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_actual_change_request_capacity_by_task_time_sheets(project_teams, task_time_sheets):
    return calculate_entities_actual_change_request_capacity_by_task_time_sheets_summing_up_by_column(
        entities=project_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_queue_length_inplace(project_teams):
    project_teams["queue_length"] = project_teams.apply(lambda x:
        x["time_left"] / x["actual_change_request_capacity"] if x["actual_change_request_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_analysis_time_left_by_tasks_time_left(project_teams, tasks):
    return calculate_entities_analysis_time_left_by_tasks_time_left_summing_up_by_column(
        entities=project_teams,
        tasks=tasks,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_actual_analysis_capacity_by_task_time_sheets(project_teams, task_time_sheets):
    return calculate_entities_actual_analysis_capacity_by_task_time_sheets_summing_up_by_column(
        entities=project_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_analysis_queue_length_inplace(project_teams):
    project_teams["analysis_queue_length"] = project_teams.apply(lambda x:
        x["analysis_time_left"] / x["actual_analysis_capacity"] if x["actual_analysis_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_development_time_left_by_tasks_time_left(project_teams, tasks):
    return calculate_entities_development_time_left_by_tasks_time_left_summing_up_by_column(
        entities=project_teams,
        tasks=tasks,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_actual_development_capacity_by_task_time_sheets(project_teams, task_time_sheets):
    return calculate_entities_actual_development_capacity_by_task_time_sheets_summing_up_by_column(
        entities=project_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_development_queue_length_inplace(project_teams):
    project_teams["development_queue_length"] = project_teams.apply(lambda x:
        x["development_time_left"] / x["actual_development_capacity"] if x["actual_development_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_testing_time_left_by_tasks_time_left(project_teams, tasks):
    return calculate_entities_testing_time_left_by_tasks_time_left_summing_up_by_column(
        entities=project_teams,
        tasks=tasks,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_actual_testing_capacity_by_task_time_sheets(project_teams, task_time_sheets):
    return calculate_entities_actual_testing_capacity_by_task_time_sheets_summing_up_by_column(
        entities=project_teams,
        task_time_sheets=task_time_sheets,
        sum_up_by_column="project_team_id"
    )

def calculate_project_teams_testing_queue_length_inplace(project_teams):
    project_teams["testing_queue_length"] = project_teams.apply(lambda x:
        x["testing_time_left"] / x["actual_testing_capacity"] if x["actual_testing_capacity"] > 0 else 0,
        axis=1
    )
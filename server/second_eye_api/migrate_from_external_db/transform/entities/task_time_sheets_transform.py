from second_eye_api.migrate_from_external_db.transform.utils import *

def replace_broken_task_time_sheet_task_id_to_task_id_with_minus_one(task_time_sheets, tasks):
    valid_task_ids = tasks['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=task_time_sheets,
        column_name="task_id",
        valid_list=valid_task_ids
    )

def replace_broken_task_time_sheet_person_id_to_person_id_with_minus_one(task_time_sheets, persons):
    valid_person_ids = persons['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=task_time_sheets,
        column_name="person_id",
        valid_list=valid_person_ids
    )

def propagate_task_skill_id_into_task_time_sheets(task_time_sheets, tasks):
    task_id_to_skill_id_mapping = tasks[["id", "skill_id"]].rename(
        columns={"id": "task_id"}
    )

    return task_time_sheets.merge(
        task_id_to_skill_id_mapping,
        how="left",
        on="task_id",
        suffixes=(None, ""),
    )

def propagate_task_planning_period_id_id_into_task_time_sheets(task_time_sheets, tasks):
    task_id_to_planning_period_id_mapping = tasks[["id", "planning_period_id"]].rename(
        columns={"id": "task_id"}
    )

    return task_time_sheets.merge(
        task_id_to_planning_period_id_mapping,
        how="left",
        on="task_id",
        suffixes=(None, ""),
    )

def propagate_task_system_change_request_id_into_task_time_sheets(task_time_sheets, tasks):
    task_id_to_system_change_request_id_mapping = tasks[["id", "system_change_request_id"]].rename(
        columns={"id": "task_id"}
    )

    return task_time_sheets.merge(
        task_id_to_system_change_request_id_mapping,
        how="left",
        on="task_id",
        suffixes=(None, ""),
    )

def propagate_system_change_request_change_request_id_into_task_time_sheets(task_time_sheets, system_change_requests):
    system_change_request_id_to_change_request_id_mapping = system_change_requests[["id", "change_request_id"]].rename(
        columns={"id": "system_change_request_id"}
    )

    return task_time_sheets.merge(
        system_change_request_id_to_change_request_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_change_request_project_team_id_into_task_time_sheets(task_time_sheets, change_requests):
    change_request_id_to_project_team_id_mapping = change_requests[["id", "project_team_id"]].rename(
        columns={"id": "change_request_id"}
    )

    return task_time_sheets.merge(
        change_request_id_to_project_team_id_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def propagate_change_request_has_value_into_task_time_sheets(task_time_sheets, change_requests):
    change_request_id_to_has_value_mapping = change_requests[["id", "has_value"]].rename(
        columns={"id": "change_request_id"}
    )

    return task_time_sheets.merge(
        change_request_id_to_has_value_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def propagate_project_team_dedicated_team_id_into_task_time_sheets(task_time_sheets, project_teams):
    dedicated_team_id_id_to_project_team_id_mapping = project_teams[["id", "dedicated_team_id"]].rename(
        columns={"id": "project_team_id"}
    )

    return task_time_sheets.merge(
        dedicated_team_id_id_to_project_team_id_mapping,
        how="left",
        on="project_team_id",
        suffixes=(None, ""),
    )

def propagate_dedicated_team_planning_period_id_into_task_time_sheets(task_time_sheets, tasks):
    task_id_to_dedicated_team_planning_period_id_mapping = tasks[["id", "dedicated_team_planning_period_id"]].rename(
        columns={"id": "task_id"}
    )

    return task_time_sheets.merge(
        task_id_to_dedicated_team_planning_period_id_mapping,
        how="left",
        on="task_id",
        suffixes=(None, ""),
    )

def propagate_project_team_planning_period_id_into_task_time_sheets(task_time_sheets, tasks):
    task_id_to_project_team_planning_period_id_mapping = tasks[["id", "project_team_planning_period_id"]].rename(
        columns={"id": "task_id"}
    )

    return task_time_sheets.merge(
        task_id_to_project_team_planning_period_id_mapping,
        how="left",
        on="task_id",
        suffixes=(None, ""),
    )
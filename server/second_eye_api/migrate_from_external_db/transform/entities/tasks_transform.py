from second_eye_api.migrate_from_external_db.transform.utils import *
from second_eye_api.models import StateCategory
from second_eye_api.models import Skill
import pandas as pd

def replace_broken_task_system_change_request_id_to_system_change_request_id_with_minus_one(tasks, system_change_requests):
    valid_system_change_request_ids = system_change_requests['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=tasks,
        column_name="system_change_request_id",
        valid_list=valid_system_change_request_ids
    )

def propagate_state_category_id_into_tasks(tasks, states):
    state_id_to_category_id_mapping = states[["id", "category_id"]].rename(columns={"id": "state_id", "category_id": "state_category_id"})

    return tasks.merge(
        state_id_to_category_id_mapping,
        how="left",
        on="state_id",
        suffixes=(None, ""),
    )

def calculate_tasks_time_spent_by_task_time_sheets(tasks, task_time_sheets):
    tasks_time_sheets_aggregated_by_task_id = task_time_sheets.groupby(
        ["task_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "task_id": "id",
        },
    )

    tasks = tasks.merge(
        tasks_time_sheets_aggregated_by_task_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    tasks["time_spent"].fillna(0, inplace=True)

    return tasks

def calculate_tasks_estimate_using_time_spent_state_category_id_planned_estimate_and_preliminary_estimate_inplace(tasks):
    tasks['estimate'] = tasks.apply(lambda x:
        x['time_spent'] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['planned_estimate'] if not pd.isnull(x['planned_estimate']) else (
                    x['preliminary_estimate'] if not pd.isnull(
                        x['preliminary_estimate']) else 0
                ),
                x['time_spent']
            )
        ), axis=1)

def calculate_tasks_time_left_using_estimate_and_time_spent_inplace(tasks):
    tasks['time_left'] = tasks.apply(lambda x: x['estimate'] - x['time_spent'], axis=1)

def propagate_system_change_requests_system_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_system_id_mapping = system_change_requests[["id", "system_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_system_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_system_change_requests_dedicated_team_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_dedicated_team_id_mapping = system_change_requests[["id", "dedicated_team_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_dedicated_team_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_system_change_requests_project_team_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_project_team_id_mapping = system_change_requests[["id", "project_team_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_project_team_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_system_change_requests_change_request_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_change_request_id_mapping = system_change_requests[["id", "change_request_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_change_request_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_system_change_requests_planning_period_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_planning_period_id_mapping = system_change_requests[["id", "planning_period_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_planning_period_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def propagate_system_change_requests_has_value_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_has_value_mapping = system_change_requests[["id", "has_value"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_has_value_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )

def make_filler_analysis_tasks_summing_up_to_system_change_request_analysis_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_analysis_tasks = system_change_requests[
        system_change_requests["analysis_estimate"] > system_change_requests["analysis_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_analysis_tasks[[
        "id",
        "analysis_tasks_estimate_sum",
        "analysis_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["analysis_estimate"] - additional_tasks["analysis_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "analysis_tasks_estimate_sum",
            "analysis_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.ANALYSIS
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = -1
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        -x.name - 1 if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_development_tasks_summing_up_to_system_change_request_development_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_development_tasks = system_change_requests[
        system_change_requests["development_estimate"] > system_change_requests["development_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_development_tasks[[
        "id",
        "development_tasks_estimate_sum",
        "development_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["development_estimate"] - additional_tasks["development_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "development_tasks_estimate_sum",
            "development_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.DEVELOPMENT
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = -1
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        -x.name - 1 if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_testing_tasks_summing_up_to_system_change_request_testing_estimate(tasks, system_change_requests):
    system_change_requests_dont_having_enough_testing_tasks = system_change_requests[
        system_change_requests["testing_estimate"] > system_change_requests["testing_tasks_estimate_sum"]]

    additional_tasks = system_change_requests_dont_having_enough_testing_tasks[[
        "id",
        "testing_tasks_estimate_sum",
        "testing_estimate",
        "system_id"
    ]].copy()

    additional_tasks["estimate"] = additional_tasks["testing_estimate"] - additional_tasks["testing_tasks_estimate_sum"]
    additional_tasks.rename(columns={"id": "system_change_request_id"}, inplace=True)
    additional_tasks.drop(
        labels=[
            "testing_tasks_estimate_sum",
            "testing_estimate"
        ],
        axis=1,
        inplace=True
    )
    additional_tasks["url"] = "https://none.com"
    additional_tasks["name"] = "Заполнитель"
    additional_tasks["skill_id"] = Skill.TESTING
    additional_tasks["system_id"] = -1
    additional_tasks["preliminary_estimate"] = additional_tasks["estimate"]
    additional_tasks["planned_estimate"] = additional_tasks["estimate"]
    additional_tasks["time_spent"] = 0
    additional_tasks["state_id"] = -1
    additional_tasks["state_category_id"] = StateCategory.TODO
    additional_tasks["time_left"] = additional_tasks["estimate"]
    additional_tasks["is_filler"] = True

    tasks = tasks.append(
        additional_tasks,
        sort=False)

    tasks.reset_index(inplace=True, drop=True) # to prevent duplicate row names

    tasks["id"] = tasks.apply(lambda x:
        -x.name - 1 if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return tasks

def make_filler_tasks_summing_up_to_system_change_request_estimate(tasks, system_change_requests):
    tasks["is_filler"] = False

    tasks = make_filler_analysis_tasks_summing_up_to_system_change_request_analysis_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    tasks = make_filler_development_tasks_summing_up_to_system_change_request_development_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    tasks = make_filler_testing_tasks_summing_up_to_system_change_request_testing_estimate(
        tasks=tasks,
        system_change_requests=system_change_requests
    )

    return tasks

def propagate_dedicated_team_planning_period_id_by_dedicated_team_id_and_planning_period_id_into_tasks(tasks, dedicated_team_planning_periods):
    dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping = dedicated_team_planning_periods[
        ["id", "dedicated_team_id", "planning_period_id"]].rename(columns={"id": "dedicated_team_planning_period_id"})

    return tasks.merge(
        dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )

def propagate_project_team_planning_period_id_by_project_team_id_and_planning_period_id_into_tasks(tasks, project_team_planning_periods):
    project_team_id_and_planning_period_id_to_project_team_planning_period_id_id_mapping = project_team_planning_periods[
        ["id", "project_team_id", "planning_period_id"]].rename(columns={"id": "project_team_planning_period_id"})

    return tasks.merge(
        project_team_id_and_planning_period_id_to_project_team_planning_period_id_id_mapping,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )

def propagate_system_change_requests_company_id_into_tasks(tasks, system_change_requests):
    system_change_request_id_to_company_id_mapping = system_change_requests[
        ["id", "company_id"]].rename(columns={"id": "system_change_request_id"})

    return tasks.merge(
        system_change_request_id_to_company_id_mapping,
        how="left",
        on="system_change_request_id",
        suffixes=(None, ""),
    )
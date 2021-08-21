from second_eye_api.migrate_from_external_db.transform.utils import *
from second_eye_api.models import Skill
from second_eye_api.models import StateCategory
import pandas as pd

def replace_broken_system_change_request_system_id_to_system_id_with_minus_one(system_change_requests, systems):
    valid_system_ids = systems['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=system_change_requests,
        column_name="system_id",
        valid_list=valid_system_ids
    )

def replace_broken_system_change_request_change_request_id_to_change_request_id_with_minus_one(system_change_requests, change_requests):
    valid_change_request_ids = change_requests['id']
    replace_column_values_with_minus_one_if_not_in_valid_list(
        dataframe=system_change_requests,
        column_name="change_request_id",
        valid_list=valid_change_request_ids
    )

def propagate_state_category_id_into_system_change_requests(system_change_requests, states):
    state_id_to_category_id_mapping = states[["id", "category_id"]].rename(columns={"id": "state_id", "category_id": "state_category_id"})

    return system_change_requests.merge(
        state_id_to_category_id_mapping,
        how="left",
        on="state_id",
        suffixes=(None, ""),
    )

def calculate_system_change_requests_analysis_tasks_estimate_sum(system_change_requests, tasks):
    analysis_tasks_estimate_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.ANALYSIS].groupby(
        ["system_change_request_id"]
    ).agg({
        "estimate": "sum"
    })
    analysis_tasks_estimate_aggregated_by_system_change_request_id.rename(columns={
        "estimate": "analysis_tasks_estimate_sum",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        analysis_tasks_estimate_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["analysis_tasks_estimate_sum"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_development_tasks_estimate_sum(system_change_requests, tasks):
    development_tasks_estimate_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.DEVELOPMENT].groupby(
        ["system_change_request_id"]
    ).agg({
        "estimate": "sum"
    })
    development_tasks_estimate_aggregated_by_system_change_request_id.rename(columns={
        "estimate": "development_tasks_estimate_sum",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        development_tasks_estimate_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["development_tasks_estimate_sum"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_testing_tasks_estimate_sum(system_change_requests, tasks):
    testing_tasks_estimate_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.TESTING].groupby(
        ["system_change_request_id"]
    ).agg({
        "estimate": "sum"
    })
    testing_tasks_estimate_aggregated_by_system_change_request_id.rename(columns={
        "estimate": "testing_tasks_estimate_sum",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        testing_tasks_estimate_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["testing_tasks_estimate_sum"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_tasks_estimate_sum_using_analysis_tasks_estimate_sum_development_tasks_estimate_sum_and_testing_tasks_estimate_sum_inplace(system_change_requests):
    system_change_requests['tasks_estimate_sum'] = \
        system_change_requests['analysis_tasks_estimate_sum'] + \
        system_change_requests['development_tasks_estimate_sum'] + \
        system_change_requests['testing_tasks_estimate_sum']

def calculate_system_change_requests_analysis_time_spent(system_change_requests, tasks):
    analysis_tasks_time_spent_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.ANALYSIS].groupby(
        ["system_change_request_id"]
    ).agg({
        "time_spent": "sum"
    })
    analysis_tasks_time_spent_aggregated_by_system_change_request_id.rename(columns={
        "time_spent": "analysis_time_spent",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        analysis_tasks_time_spent_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["analysis_time_spent"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_development_time_spent(system_change_requests, tasks):
    development_tasks_time_spent_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.DEVELOPMENT].groupby(
        ["system_change_request_id"]
    ).agg({
        "time_spent": "sum"
    })
    development_tasks_time_spent_aggregated_by_system_change_request_id.rename(columns={
        "time_spent": "development_time_spent",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        development_tasks_time_spent_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["development_time_spent"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_testing_time_spent(system_change_requests, tasks):
    testing_tasks_time_spent_aggregated_by_system_change_request_id = tasks[tasks["skill_id"] == Skill.TESTING].groupby(
        ["system_change_request_id"]
    ).agg({
        "time_spent": "sum"
    })
    testing_tasks_time_spent_aggregated_by_system_change_request_id.rename(columns={
        "time_spent": "testing_time_spent",
    }, inplace=True)

    system_change_requests = system_change_requests.merge(
        testing_tasks_time_spent_aggregated_by_system_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    system_change_requests["testing_time_spent"].fillna(0, inplace=True)

    return system_change_requests

def calculate_system_change_requests_time_spent_using_analysis_time_spent_development_time_spent_and_testing_time_spent_inplace(system_change_requests):
    system_change_requests['time_spent'] = \
        system_change_requests['analysis_time_spent'] + \
        system_change_requests['development_time_spent'] + \
        system_change_requests['testing_time_spent']

def calculate_system_change_requests_analysis_estimate_using_analysis_time_spent_state_category_id_analysis_planned_estimate_analysis_preliminary_estimate_and_analysis_tasks_estimate_sum_inplace(system_change_requests):
    system_change_requests['analysis_estimate'] = system_change_requests.apply(lambda x:
        x['analysis_time_spent'] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['analysis_planned_estimate'] if not pd.isnull(x['analysis_planned_estimate']) else (
                    x['analysis_preliminary_estimate'] if not pd.isnull(x['analysis_preliminary_estimate']) else 0
                ),
                x['analysis_tasks_estimate_sum'],
                x['analysis_time_spent']
            )
        ), axis=1)

def calculate_system_change_requests_development_estimate_using_development_time_spent_state_category_id_development_planned_estimate_development_preliminary_estimate_and_development_tasks_estimate_sum_inplace(system_change_requests):
    system_change_requests['development_estimate'] = system_change_requests.apply(lambda x:
        x['development_time_spent'] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['development_planned_estimate'] if not pd.isnull(x['development_planned_estimate']) else (
                    x['development_preliminary_estimate'] if not pd.isnull(x['development_preliminary_estimate']) else 0
                ),
                x['development_tasks_estimate_sum'],
                x['development_time_spent']
            )
        ), axis=1)

def calculate_system_change_requests_testing_estimate_using_testing_time_spent_state_category_id_testing_planned_estimate_testing_preliminary_estimate_and_testing_tasks_estimate_inplace(system_change_requests):
    system_change_requests['testing_estimate'] = system_change_requests.apply(lambda x:
        x['testing_time_spent'] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['testing_planned_estimate'] if not pd.isnull(x['testing_planned_estimate']) else (
                    x['testing_preliminary_estimate'] if not pd.isnull(x['testing_preliminary_estimate']) else 0
                ),
                x['testing_tasks_estimate_sum'],
                x['testing_time_spent']
            )
        ), axis=1)

def calculate_system_change_requests_estimate_using_analysis_estimate_development_estimate_and_testing_estimate_inplace(system_change_requests):
    system_change_requests['estimate'] = \
        system_change_requests['analysis_estimate'] + \
        system_change_requests['development_estimate'] + \
        system_change_requests['testing_estimate']

def calculate_system_change_requests_time_left_using_estimate_and_time_spent_inplace(system_change_requests):
    system_change_requests['time_left'] = system_change_requests['estimate'] - system_change_requests['time_spent']


def calculate_system_change_requests_analysis_time_left_using_analysis_estimate_and_analysis_time_spent_inplace(system_change_requests):
    system_change_requests['analysis_time_left'] = \
        system_change_requests['analysis_estimate'] - system_change_requests['analysis_time_spent']

def calculate_system_change_requests_development_time_left_using_development_estimate_and_development_time_spent_inplace(system_change_requests):
    system_change_requests['development_time_left'] = \
        system_change_requests['development_estimate'] - system_change_requests['development_time_spent']

def calculate_system_change_requests_testing_time_left_using_testing_estimate_and_testing_time_spent_inplace(system_change_requests):
    system_change_requests['testing_time_left'] = \
        system_change_requests['testing_estimate'] - system_change_requests['testing_time_spent']

def calculate_system_change_requests_time_left_using_estimate_and_time_left_inplace(system_change_requests):
    system_change_requests['time_left'] = \
        system_change_requests['estimate'] - system_change_requests['time_spent']

def propagate_change_requests_dedicated_team_id_into_system_change_requests(system_change_requests, change_requests):
    change_request_id_to_dedicated_team_id_mapping = change_requests[["id", "dedicated_team_id"]].rename(columns={"id": "change_request_id"})

    return system_change_requests.merge(
        change_request_id_to_dedicated_team_id_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def propagate_change_requests_project_team_id_into_system_change_requests(system_change_requests, change_requests):
    change_request_id_to_project_team_id_mapping = change_requests[["id", "project_team_id"]].rename(columns={"id": "change_request_id"})

    return system_change_requests.merge(
        change_request_id_to_project_team_id_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def propagate_change_requests_planning_period_id_into_system_change_requests(system_change_requests, change_requests):
    change_request_id_to_planning_period_id_mapping = change_requests[["id", "planning_period_id"]].rename(columns={"id": "change_request_id"})

    return system_change_requests.merge(
        change_request_id_to_planning_period_id_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def propagate_change_requests_has_value_into_system_change_requests(system_change_requests, change_requests):
    change_request_id_to_has_value_mapping = change_requests[["id", "has_value"]].rename(columns={"id": "change_request_id"})

    return system_change_requests.merge(
        change_request_id_to_has_value_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )

def make_filler_system_change_requests_summing_up_to_change_request_estimate(system_change_requests, change_requests):
    system_change_requests["is_filler"] = False

    change_requests_dont_having_enough_change_requests = change_requests[change_requests["estimate"] > change_requests["system_change_requests_estimate_sum"]]

    additional_system_change_requests = change_requests_dont_having_enough_change_requests[[
        "id",
        "estimate",
        "system_change_requests_estimate_sum",
        "analysis_estimate",
        "system_change_requests_analysis_estimate_sum",
        "development_estimate",
        "system_change_requests_development_estimate_sum",
        "testing_estimate",
        "system_change_requests_testing_estimate_sum"
    ]].copy()

    additional_system_change_requests["estimate"] = additional_system_change_requests["estimate"] - additional_system_change_requests["system_change_requests_estimate_sum"]
    additional_system_change_requests["analysis_estimate"] = additional_system_change_requests["analysis_estimate"] - additional_system_change_requests["system_change_requests_analysis_estimate_sum"]
    additional_system_change_requests["development_estimate"] = additional_system_change_requests["development_estimate"] - additional_system_change_requests["system_change_requests_development_estimate_sum"]
    additional_system_change_requests["testing_estimate"] = additional_system_change_requests["testing_estimate"] - additional_system_change_requests["system_change_requests_testing_estimate_sum"]
    additional_system_change_requests.rename(columns={"id": "change_request_id"}, inplace=True)
    additional_system_change_requests.drop(
        labels=[
            "system_change_requests_estimate_sum",
            "system_change_requests_analysis_estimate_sum",
            "system_change_requests_development_estimate_sum",
            "system_change_requests_testing_estimate_sum"
        ],
        axis=1,
        inplace=True
    )
    additional_system_change_requests["url"] = "https://none.com"
    additional_system_change_requests["name"] = "Заполнитель"
    additional_system_change_requests["system_id"] = -1
    additional_system_change_requests["analysis_preliminary_estimate"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_preliminary_estimate"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_preliminary_estimate"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["analysis_planned_estimate"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_planned_estimate"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_planned_estimate"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["state_id"] = -1
    additional_system_change_requests["state_category_id"] = StateCategory.TODO
    additional_system_change_requests["analysis_tasks_estimate_sum"] = 0
    additional_system_change_requests["development_tasks_estimate_sum"] = 0
    additional_system_change_requests["testing_tasks_estimate_sum"] = 0
    additional_system_change_requests["tasks_estimate_sum"] = 0
    additional_system_change_requests["analysis_time_spent"] = 0
    additional_system_change_requests["development_time_spent"] = 0
    additional_system_change_requests["testing_time_spent"] = 0
    additional_system_change_requests["time_spent"] = 0
    additional_system_change_requests["analysis_time_left"] = additional_system_change_requests["analysis_estimate"]
    additional_system_change_requests["development_time_left"] = additional_system_change_requests["development_estimate"]
    additional_system_change_requests["testing_time_left"] = additional_system_change_requests["testing_estimate"]
    additional_system_change_requests["time_left"] = additional_system_change_requests["estimate"]
    additional_system_change_requests["is_filler"] = True

    system_change_requests = system_change_requests.append(
        additional_system_change_requests,
        sort=False)

    system_change_requests.reset_index(inplace=True, drop=True)  # to prevent duplicate row names

    system_change_requests["id"] = system_change_requests.apply(lambda x:
        -x.name - 1 if pd.isnull(x["id"]) else x["id"],
        axis=1
    )

    return system_change_requests

def propagate_change_requests_company_id_into_system_change_requests(system_change_requests, change_requests):
    change_request_id_to_company_id_mapping = change_requests[["id", "company_id"]].rename(
        columns={"id": "change_request_id"})

    return system_change_requests.merge(
        change_request_id_to_company_id_mapping,
        how="left",
        on="change_request_id",
        suffixes=(None, ""),
    )
from second_eye_api.models import StateCategory
from second_eye_api.models import Skill
import pandas as pd

def propagate_state_category_id_into_change_requests(change_requests, states):
    state_id_to_category_id_mapping = states[["id", "category_id"]].rename(columns={"id": "state_id", "category_id": "state_category_id"})

    return change_requests.merge(
        state_id_to_category_id_mapping,
        how="left",
        on="state_id",
        suffixes=(None, ""),
    )

def calculate_change_requests_system_change_requests_analysis_estimate_sum(change_requests, system_change_requests):
    system_change_requests_analysis_estimate_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "analysis_estimate": "sum"
    })
    system_change_requests_analysis_estimate_aggregated_by_change_request_id.rename(columns={
        "analysis_estimate": "system_change_requests_analysis_estimate_sum",
    }, inplace=True)

    change_requests = change_requests.merge(
        system_change_requests_analysis_estimate_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["system_change_requests_analysis_estimate_sum"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_system_change_requests_development_estimate_sum(change_requests, system_change_requests):
    system_change_requests_development_estimate_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "development_estimate": "sum"
    })
    system_change_requests_development_estimate_aggregated_by_change_request_id.rename(columns={
        "development_estimate": "system_change_requests_development_estimate_sum",
    }, inplace=True)

    change_requests = change_requests.merge(
        system_change_requests_development_estimate_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["system_change_requests_development_estimate_sum"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_system_change_requests_testing_estimate_sum(change_requests, system_change_requests):
    system_change_requests_testing_estimate_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "testing_estimate": "sum"
    })
    system_change_requests_testing_estimate_aggregated_by_change_request_id.rename(columns={
        "testing_estimate": "system_change_requests_testing_estimate_sum",
    }, inplace=True)

    change_requests = change_requests.merge(
        system_change_requests_testing_estimate_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["system_change_requests_testing_estimate_sum"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_system_change_requests_estimate_sum_using_system_change_requests_analysis_development_and_testing_estimate_sum(change_requests):
    change_requests["system_change_requests_estimate_sum"] = \
          change_requests["system_change_requests_analysis_estimate_sum"] \
        + change_requests["system_change_requests_development_estimate_sum"] \
        + change_requests["system_change_requests_testing_estimate_sum"]

def calculate_change_requests_analysis_time_spent_sum(change_requests, system_change_requests):
    system_change_requests_analysis_time_spent_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "analysis_time_spent": "sum"
    })

    change_requests = change_requests.merge(
        system_change_requests_analysis_time_spent_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["analysis_time_spent"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_development_time_spent_sum(change_requests, system_change_requests):
    system_change_requests_development_time_spent_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "development_time_spent": "sum"
    })

    change_requests = change_requests.merge(
        system_change_requests_development_time_spent_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["development_time_spent"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_testing_time_spent_sum(change_requests, system_change_requests):
    system_change_requests_testing_time_spent_aggregated_by_change_request_id = system_change_requests.groupby(
        ["change_request_id"]
    ).agg({
        "testing_time_spent": "sum"
    })

    change_requests = change_requests.merge(
        system_change_requests_testing_time_spent_aggregated_by_change_request_id,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, ""),
    )

    change_requests["testing_time_spent"].fillna(0, inplace=True)

    return change_requests

def calculate_change_requests_time_spent_using_analysis_development_and_testing_time_spent_inplace(change_requests):
    change_requests["time_spent"] = \
          change_requests["analysis_time_spent"] \
        + change_requests["development_time_spent"] \
        + change_requests["testing_time_spent"]

def calculate_change_requests_analysis_estimate_using_analysis_time_spent_state_category_id_analysis_express_estimate_and_system_change_requests_analysis_estimate_sum_inplace(change_requests):
    change_requests["analysis_estimate"] = change_requests.apply(lambda x:
        x["analysis_time_spent"] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['analysis_express_estimate'] if not pd.isnull(x['analysis_express_estimate']) else 0,
                x['system_change_requests_analysis_estimate_sum'],
                x['analysis_time_spent']
            )
        ), axis=1)

def calculate_change_requests_development_estimate_using_development_time_spent_state_category_id_development_express_estimate_and_system_change_requests_development_estimate_sum_inplace(change_requests):
    change_requests["development_estimate"] = change_requests.apply(lambda x:
        x["development_time_spent"] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['development_express_estimate'] if not pd.isnull(x['development_express_estimate']) else 0,
                x['system_change_requests_development_estimate_sum'],
                x['development_time_spent']
            )
        ), axis=1)

def calculate_change_requests_testing_estimate_using_testing_time_spent_state_category_id_testing_express_estimate_and_system_change_requests_testing_estimate_sum_inplace(change_requests):
    change_requests["testing_estimate"] = change_requests.apply(lambda x:
        x["testing_time_spent"] if x['state_category_id'] == StateCategory.DONE else (
            max(
                x['testing_express_estimate'] if not pd.isnull(x['testing_express_estimate']) else 0,
                x['system_change_requests_testing_estimate_sum'],
                x['testing_time_spent']
            )
        ), axis=1)

def calculate_change_requests_estimate_using_analysis_development_and_testing_estimate_inplace(change_requests):
    change_requests["estimate"] = \
          change_requests["analysis_estimate"] \
        + change_requests["development_estimate"] \
        + change_requests["testing_estimate"]

def calculate_change_requests_analyis_time_left_using_analysis_estimate_and_analysis_time_spent_inplace(change_requests):
    change_requests["analysis_time_left"] = change_requests["analysis_estimate"] - change_requests["analysis_time_spent"]

def calculate_change_requests_development_time_left_using_development_estimate_and_development_time_spent_inplace(change_requests):
    change_requests["development_time_left"] = change_requests["development_estimate"] - change_requests["development_time_spent"]

def calculate_change_requests_testing_time_left_using_testing_estimate_and_testing_time_spent_inplace(change_requests):
    change_requests["testing_time_left"] = change_requests["testing_estimate"] - change_requests["testing_time_spent"]

def calculate_change_requests_time_left_using_analysis_development_and_testing_time_left(change_requests):
    change_requests["time_left"] = \
          change_requests["analysis_time_left"] \
        + change_requests["development_time_left"] \
        + change_requests["testing_time_left"]

def calculate_change_requests_planning_period_using_planning_period_id_planned_install_date_and_year_label_max_inplace(change_requests):
    change_requests["planning_period_id"] = change_requests.apply(lambda x:
        pd.to_datetime(x["planned_install_date"]).year if not pd.isnull(x["planned_install_date"]) else (x["year_label_max"] if not pd.isnull(x["year_label_max"]) else - 1),
        axis=1
    )

def propagate_project_teams_dedicated_team_id_into_change_requests(change_requests, project_teams):
    project_team_id_to_dedicated_team_id_mapping = project_teams[["id", "dedicated_team_id"]].rename(columns={"id": "project_team_id"})

    return change_requests.merge(
        project_team_id_to_dedicated_team_id_mapping,
        how="left",
        on="project_team_id",
        suffixes=(None, ""),
    )

def propagate_dedicated_team_planning_period_id_into_change_requests(change_requests, dedicated_team_planning_periods):
    dedicated_team_planning_period_id_to_dedicated_team_id_mapping = dedicated_team_planning_periods[
        ["id", "dedicated_team_id", "planning_period_id"]].rename(columns={"id": "dedicated_team_planning_period_id"})

    return change_requests.merge(
        dedicated_team_planning_period_id_to_dedicated_team_id_mapping,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )

def propagate_project_team_planning_period_id_into_change_requests(change_requests, project_team_planning_periods):
    project_team_planning_period_id_to_project_team_id_mapping = project_team_planning_periods[
        ["id", "project_team_id", "planning_period_id"]].rename(columns={"id": "project_team_planning_period_id"})

    return change_requests.merge(
        project_team_planning_period_id_to_project_team_id_mapping,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )

def propagate_project_teams_company_id_into_change_requests(change_requests, project_teams):
    project_team_id_to_company_id_mapping = project_teams[["id", "company_id"]].rename(columns={"id": "project_team_id"})

    return change_requests.merge(
        project_team_id_to_company_id_mapping,
        how="left",
        on="project_team_id",
        suffixes=(None, ""),
    )

def calculate_change_requests_effort_by_time_left_inplace_(change_requests):
    change_requests["effort"] = change_requests["time_left"] / 8

def calculate_change_requests_actual_change_request_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    number_of_days_in_period = 28
    look_behind = 7
    work_days = 5
    week_days = 7
    hours_per_day = 8
    today = pd.to_datetime('today').normalize()
    start = today - pd.to_timedelta("{}day".format(number_of_days_in_period + look_behind))
    end = today - pd.to_timedelta("{}day".format(look_behind))

    task_time_sheets_behind = task_time_sheets[
        (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    tasks_time_sheets_aggregated_by_change_request_id = task_time_sheets_behind.groupby(
        ["change_request_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "change_request_id": "id",
            "time_spent": "time_spent_last_period"
        },
    )

    change_requests = change_requests.merge(
        tasks_time_sheets_aggregated_by_change_request_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    change_requests["time_spent_last_period"].fillna(0, inplace=True)
    change_requests["actual_change_request_capacity"] = change_requests["time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return change_requests

def calculate_change_requests_queue_length_inplace(change_requests):
    change_requests["queue_length"] = change_requests.apply(lambda x:
        x["effort"] / x["actual_change_request_capacity"] if x["actual_change_request_capacity"] > 0 else 0,
        axis=1
    )

def calculate_change_requests_analysis_effort_by_time_left_inplace_(change_requests):
    change_requests["analysis_effort"] = change_requests["analysis_time_left"] / 8

def calculate_change_requests_actual_analysis_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    number_of_days_in_period = 28
    look_behind = 7
    work_days = 5
    week_days = 7
    hours_per_day = 8
    today = pd.to_datetime('today').normalize()
    start = today - pd.to_timedelta("{}day".format(number_of_days_in_period + look_behind))
    end = today - pd.to_timedelta("{}day".format(look_behind))

    analysis_task_time_sheets_behind = task_time_sheets[
        (task_time_sheets["skill_id"] == Skill.ANALYSIS)
        & (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    analysis_tasks_time_sheets_aggregated_by_change_request_id = analysis_task_time_sheets_behind.groupby(
        ["change_request_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "change_request_id": "id",
            "time_spent": "analysis_time_spent_last_period"
        },
    )

    change_requests = change_requests.merge(
        analysis_tasks_time_sheets_aggregated_by_change_request_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    change_requests["analysis_time_spent_last_period"].fillna(0, inplace=True)
    change_requests["actual_analysis_capacity"] = change_requests["analysis_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return change_requests

def calculate_change_requests_analysis_queue_length_inplace(change_requests):
    change_requests["analysis_queue_length"] = change_requests.apply(lambda x:
        x["analysis_effort"] / x["actual_analysis_capacity"] if x["actual_analysis_capacity"] > 0 else 0,
        axis=1
    )

def calculate_change_requests_development_effort_by_time_left_inplace_(change_requests):
    change_requests["development_effort"] = change_requests["development_time_left"] / 8

def calculate_change_requests_actual_developmen_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    number_of_days_in_period = 28
    look_behind = 7
    work_days = 5
    week_days = 7
    hours_per_day = 8
    today = pd.to_datetime('today').normalize()
    start = today - pd.to_timedelta("{}day".format(number_of_days_in_period + look_behind))
    end = today - pd.to_timedelta("{}day".format(look_behind))

    development_task_time_sheets_behind = task_time_sheets[
        (task_time_sheets["skill_id"] == Skill.DEVELOPMENT)
        & (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    development_tasks_time_sheets_aggregated_by_change_request_id = development_task_time_sheets_behind.groupby(
        ["change_request_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "change_request_id": "id",
            "time_spent": "development_time_spent_last_period"
        },
    )

    change_requests = change_requests.merge(
        development_tasks_time_sheets_aggregated_by_change_request_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    change_requests["development_time_spent_last_period"].fillna(0, inplace=True)
    change_requests["actual_development_capacity"] = change_requests["development_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return change_requests

def calculate_change_requests_development_queue_length_inplace(change_requests):
    change_requests["development_queue_length"] = change_requests.apply(lambda x:
        x["development_effort"] / x["actual_development_capacity"] if x["actual_development_capacity"] > 0 else 0,
        axis=1
    )

def calculate_change_requests_testing_effort_by_time_left_inplace_(change_requests):
    change_requests["testing_effort"] = change_requests["testing_time_left"] / 8

def calculate_change_requests_actual_testing_capacity_by_task_time_sheets(change_requests, task_time_sheets):
    number_of_days_in_period = 28
    look_behind = 7
    work_days = 5
    week_days = 7
    hours_per_day = 8
    today = pd.to_datetime('today').normalize()
    start = today - pd.to_timedelta("{}day".format(number_of_days_in_period + look_behind))
    end = today - pd.to_timedelta("{}day".format(look_behind))

    testing_task_time_sheets_behind = task_time_sheets[
        (task_time_sheets["skill_id"] == Skill.TESTING)
        & (task_time_sheets["date"] >= start)
        & (task_time_sheets["date"] < end)
    ].copy()

    testing_tasks_time_sheets_aggregated_by_change_request_id = testing_task_time_sheets_behind.groupby(
        ["change_request_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "change_request_id": "id",
            "time_spent": "testing_time_spent_last_period"
        },
    )

    change_requests = change_requests.merge(
        testing_tasks_time_sheets_aggregated_by_change_request_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    change_requests["testing_time_spent_last_period"].fillna(0, inplace=True)
    change_requests["actual_testing_capacity"] = change_requests["testing_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return change_requests

def calculate_change_requests_testing_queue_length_inplace(change_requests):
    change_requests["testing_queue_length"] = change_requests.apply(lambda x:
        x["testing_effort"] / x["actual_testing_capacity"] if x["actual_testing_capacity"] > 0 else 0,
        axis=1
    )

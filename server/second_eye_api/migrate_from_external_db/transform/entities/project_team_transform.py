import pandas as pd

from second_eye_api.models import Skill

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
    tasks_time_left_aggregated_by_project_team_id = tasks.groupby(
        ["project_team_id"]
    ).agg({
        "time_left": "sum"
    }).reset_index().rename(
        columns={"project_team_id": "id"},
    )

    project_teams = project_teams.merge(
        tasks_time_left_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["time_left"].fillna(0, inplace=True)

    return project_teams

def calculate_project_teams_effort_by_time_left_inplace_(project_teams):
    project_teams["effort"] = project_teams["time_left"] / 8

def calculate_project_teams_actual_change_request_capacity_by_task_time_sheets(project_teams, task_time_sheets):
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

    tasks_time_sheets_aggregated_by_project_team_id = task_time_sheets_behind.groupby(
        ["project_team_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_spent": "time_spent_last_period"
        },
    )

    project_teams = project_teams.merge(
        tasks_time_sheets_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["time_spent_last_period"].fillna(0, inplace=True)
    project_teams["actual_change_request_capacity"] = project_teams["time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return project_teams

def calculate_project_teams_queue_length_inplace(project_teams):
    project_teams["queue_length"] = project_teams.apply(lambda x:
        x["effort"] / x["actual_change_request_capacity"] if x["actual_change_request_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_analysis_time_left_by_tasks_time_left(project_teams, tasks):
    tasks_analysis_time_left_aggregated_by_project_team_id = tasks[tasks["skill_id"] == Skill.ANALYSIS].groupby(
        ["project_team_id"]
    ).agg({
        "time_left": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_left": "analysis_time_left"
        },
    )

    project_teams = project_teams.merge(
        tasks_analysis_time_left_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["analysis_time_left"].fillna(0, inplace=True)

    return project_teams

def calculate_project_teams_analysis_effort_by_time_left_inplace_(project_teams):
    project_teams["analysis_effort"] = project_teams["analysis_time_left"] / 8

def calculate_project_teams_actual_analysis_capacity_by_task_time_sheets(project_teams, task_time_sheets):
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

    analysis_tasks_time_sheets_aggregated_by_project_team_id = analysis_task_time_sheets_behind.groupby(
        ["project_team_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_spent": "analysis_time_spent_last_period"
        },
    )

    project_teams = project_teams.merge(
        analysis_tasks_time_sheets_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["analysis_time_spent_last_period"].fillna(0, inplace=True)
    project_teams["actual_analysis_capacity"] = project_teams["analysis_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return project_teams

def calculate_project_teams_analysis_queue_length_inplace(project_teams):
    project_teams["analysis_queue_length"] = project_teams.apply(lambda x:
        x["analysis_effort"] / x["actual_analysis_capacity"] if x["actual_analysis_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_development_time_left_by_tasks_time_left(project_teams, tasks):
    tasks_development_time_left_aggregated_by_project_team_id = tasks[tasks["skill_id"] == Skill.DEVELOPMENT].groupby(
        ["project_team_id"]
    ).agg({
        "time_left": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_left": "development_time_left"
        },
    )

    project_teams = project_teams.merge(
        tasks_development_time_left_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["development_time_left"].fillna(0, inplace=True)

    return project_teams

def calculate_project_teams_development_effort_by_time_left_inplace_(project_teams):
    project_teams["development_effort"] = project_teams["development_time_left"] / 8

def calculate_project_teams_actual_developmen_capacity_by_task_time_sheets(project_teams, task_time_sheets):
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

    development_tasks_time_sheets_aggregated_by_project_team_id = development_task_time_sheets_behind.groupby(
        ["project_team_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_spent": "development_time_spent_last_period"
        },
    )

    project_teams = project_teams.merge(
        development_tasks_time_sheets_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["development_time_spent_last_period"].fillna(0, inplace=True)
    project_teams["actual_development_capacity"] = project_teams["development_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return project_teams

def calculate_project_teams_development_queue_length_inplace(project_teams):
    project_teams["development_queue_length"] = project_teams.apply(lambda x:
        x["development_effort"] / x["actual_development_capacity"] if x["actual_development_capacity"] > 0 else 0,
        axis=1
    )

def calculate_project_teams_testing_time_left_by_tasks_time_left(project_teams, tasks):
    tasks_testing_time_left_aggregated_by_project_team_id = tasks[tasks["skill_id"] == Skill.TESTING].groupby(
        ["project_team_id"]
    ).agg({
        "time_left": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_left": "testing_time_left"
        },
    )

    project_teams = project_teams.merge(
        tasks_testing_time_left_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["testing_time_left"].fillna(0, inplace=True)

    return project_teams

def calculate_project_teams_testing_effort_by_time_left_inplace_(project_teams):
    project_teams["testing_effort"] = project_teams["testing_time_left"] / 8

def calculate_project_teams_actual_testing_capacity_by_task_time_sheets(project_teams, task_time_sheets):
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

    testing_tasks_time_sheets_aggregated_by_project_team_id = testing_task_time_sheets_behind.groupby(
        ["project_team_id"]
    ).agg({
        "time_spent": "sum"
    }).reset_index().rename(
        columns={
            "project_team_id": "id",
            "time_spent": "testing_time_spent_last_period"
        },
    )

    project_teams = project_teams.merge(
        testing_tasks_time_sheets_aggregated_by_project_team_id,
        how="left",
        on="id",
        suffixes=(False, ""),
    )

    project_teams["testing_time_spent_last_period"].fillna(0, inplace=True)
    project_teams["actual_testing_capacity"] = project_teams["testing_time_spent_last_period"] / number_of_days_in_period * week_days / work_days / hours_per_day

    return project_teams

def calculate_project_teams_testing_queue_length_inplace(project_teams):
    project_teams["testing_queue_length"] = project_teams.apply(lambda x:
        x["testing_effort"] / x["actual_testing_capacity"] if x["actual_testing_capacity"] > 0 else 0,
        axis=1
    )
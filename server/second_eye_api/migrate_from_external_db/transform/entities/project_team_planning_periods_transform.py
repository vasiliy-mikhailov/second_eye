import pandas as pd
from ..utils import linear_polyfit

def calculate_project_team_planning_periods_from_change_requests_planning_period_id_and_project_team_id(change_requests):
    result = change_requests.groupby(["dedicated_team_id", "planning_period_id", "project_team_id"]).size().reset_index(name="count")
    result["id"] = result.apply(lambda x:
        -1 if x["planning_period_id"] == -1 and x["project_team_id"] == -1 else x.name + 1,
        axis=1
    )
    return result

def calculate_project_team_planning_periods_estimate_by_tasks_estimate(project_team_planning_periods, tasks):
    tasks_estimate_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "estimate": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_estimate_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["estimate"].fillna(0, inplace=True)

    return project_team_planning_periods

def calculate_project_team_planning_periods_time_spent_by_tasks_time_spent(project_team_planning_periods, tasks):
    tasks_time_spent_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "time_spent": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_time_spent_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["time_spent"].fillna(0, inplace=True)

    return project_team_planning_periods

def calculate_project_team_planning_periods_time_left_by_tasks_time_left(project_team_planning_periods, tasks):
    tasks_time_left_aggregated_by_project_team_id_and_planning_period_id = tasks.groupby(
        ["project_team_id", "planning_period_id"]
    ).agg({
        "time_left": "sum"
    })

    project_team_planning_periods = project_team_planning_periods.merge(
        tasks_time_left_aggregated_by_project_team_id_and_planning_period_id,
        how="left",
        on=["project_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    project_team_planning_periods["time_left"].fillna(0, inplace=True)

    return project_team_planning_periods

def propagate_dedicated_team_planning_period_id_by_dedicated_team_id_and_planning_period_id_into_project_team_planning_periods(
        project_team_planning_periods,
        dedicated_team_planning_periods
):
    dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping = dedicated_team_planning_periods[
        ["id", "dedicated_team_id", "planning_period_id"]].rename(columns={"id": "dedicated_team_planning_period_id"})

    return project_team_planning_periods.merge(
        dedicated_team_id_and_planning_period_id_to_dedicated_team_planning_period_id_id_mapping,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(None, ""),
    )

def propagate_planning_periods_start_into_project_team_planning_periods(
        project_team_planning_periods,
        planning_periods
):
    planning_periods_reduced_to_id_and_start = planning_periods[["id", "start"]].rename(columns={
        "id": "planning_period_id",
        "start": "planning_period_start",
    })

    return project_team_planning_periods.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="planning_period_id",
        suffixes=(None, ""),
    )

def propagate_planning_periods_end_into_project_team_planning_periods(
        project_team_planning_periods,
        planning_periods
):
    planning_periods_reduced_to_id_and_start = planning_periods[["id", "end"]].rename(columns={
        "id": "planning_period_id",
        "end": "planning_period_end",
    })

    return project_team_planning_periods.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="planning_period_id",
        suffixes=(None, ""),
    )

def calculate_project_team_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    project_team_planning_periods,
    project_team_planning_period_time_sheets_by_date,
):
    project_team_planning_period_task_time_sheets_filtered_by_period_start_and_end = project_team_planning_period_time_sheets_by_date[
        (project_team_planning_period_time_sheets_by_date["date"] >= project_team_planning_period_time_sheets_by_date["planning_period_start"])
        & (project_team_planning_period_time_sheets_by_date["date"] <= project_team_planning_period_time_sheets_by_date["planning_period_end"])
    ]
    model = project_team_planning_period_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["project_team_planning_period_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
    ))

    result = project_team_planning_periods.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_project_team_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        project_team_planning_periods
):
    project_team_planning_periods["time_spent_cumsum_at_end_prediction"] = 1 * project_team_planning_periods["time_sheets_by_date_model_m"] + project_team_planning_periods["time_sheets_by_date_model_b"]

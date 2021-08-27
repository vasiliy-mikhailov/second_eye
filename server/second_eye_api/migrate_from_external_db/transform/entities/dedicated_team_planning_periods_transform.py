import pandas as pd
from ..utils import linear_polyfit

def calculate_dedicated_team_planning_periods_from_change_requests_planning_period_id_and_dedicated_team(change_requests):
    result = change_requests.groupby(["planning_period_id", "dedicated_team_id"]).size().reset_index(name="count")
    result["id"] = result.apply(lambda x:
        -1 if x["planning_period_id"] == -1 and x["dedicated_team_id"] == -1 else x.name + 1,
        axis=1
    )
    return result

def calculate_dedicated_team_planning_periods_estimate_by_tasks_estimate(dedicated_team_planning_periods, tasks):
    tasks_estimate_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "estimate": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_estimate_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["estimate"].fillna(0, inplace=True)

    return dedicated_team_planning_periods

def calculate_dedicated_team_planning_periods_time_spent_by_tasks_time_spent(dedicated_team_planning_periods, tasks):
    tasks_time_spent_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "time_spent": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_time_spent_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["time_spent"].fillna(0, inplace=True)

    return dedicated_team_planning_periods

def calculate_dedicated_team_planning_periods_time_left_by_tasks_time_left(dedicated_team_planning_periods, tasks):
    tasks_time_left_aggregated_by_dedicated_team_id_and_planning_period_id = tasks.groupby(
        ["dedicated_team_id", "planning_period_id"]
    ).agg({
        "time_left": "sum"
    })

    dedicated_team_planning_periods = dedicated_team_planning_periods.merge(
        tasks_time_left_aggregated_by_dedicated_team_id_and_planning_period_id,
        how="left",
        on=["dedicated_team_id", "planning_period_id"],
        suffixes=(False, ""),
    )

    dedicated_team_planning_periods["time_left"].fillna(0, inplace=True)

    return dedicated_team_planning_periods

def propagate_planning_periods_start_into_dedicated_team_planning_periods(
        dedicated_team_planning_periods,
        planning_periods
):
    planning_periods_reduced_to_id_and_start = planning_periods[["id", "start"]].rename(columns={
        "id": "planning_period_id",
        "start": "planning_period_start",
    })

    return dedicated_team_planning_periods.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="planning_period_id",
        suffixes=(None, ""),
    )

def propagate_planning_periods_end_into_dedicated_team_planning_periods(
        dedicated_team_planning_periods,
        planning_periods
):
    planning_periods_reduced_to_id_and_start = planning_periods[["id", "end"]].rename(columns={
        "id": "planning_period_id",
        "end": "planning_period_end",
    })

    return dedicated_team_planning_periods.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="planning_period_id",
        suffixes=(None, ""),
    )

def calculate_dedicated_team_planning_periods_time_sheets_by_date_model_by_time_sheets_planning_period_start_and_planning_period_end_and_date_and_time_spent_cumsum(
    dedicated_team_planning_periods,
    dedicated_team_planning_period_time_sheets_by_date,
):
    dedicated_team_planning_period_task_time_sheets_filtered_by_period_start_and_end = dedicated_team_planning_period_time_sheets_by_date[
        (dedicated_team_planning_period_time_sheets_by_date["date"] >= dedicated_team_planning_period_time_sheets_by_date["planning_period_start"])
        & (dedicated_team_planning_period_time_sheets_by_date["date"] <= dedicated_team_planning_period_time_sheets_by_date["planning_period_end"])
    ]
    model = dedicated_team_planning_period_task_time_sheets_filtered_by_period_start_and_end.groupby(
        ["dedicated_team_planning_period_id"]
    ).apply(lambda x: pd.Series(
        linear_polyfit(
            x=(x["date"] - x["planning_period_start"]) / (x["planning_period_end"] - x["planning_period_start"]),
            y=x["time_spent_cumsum"]),
        index=["time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]
    ))

    result = dedicated_team_planning_periods.merge(
        model,
        how="left",
        left_on="id",
        right_index=True,
        suffixes=(False, "")
    )

    return result

def calculate_dedicated_team_planning_period_time_spent_cumsum_at_end_prediction_by_m_and_b_inplace(
        dedicated_team_planning_periods
):
    dedicated_team_planning_periods["time_spent_cumsum_at_end_prediction"] = 1 * dedicated_team_planning_periods["time_sheets_by_date_model_m"] + dedicated_team_planning_periods["time_sheets_by_date_model_b"]

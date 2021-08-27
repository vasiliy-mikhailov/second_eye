from ..utils import normalize

def calculate_dedicated_team_planning_period_time_sheets_by_date(task_time_sheets):
    result = task_time_sheets.copy()
    result = result[["dedicated_team_planning_period_id", "date", "time_spent"]].groupby(
        ["dedicated_team_planning_period_id", "date"]
    ).agg({"time_spent": "sum"}).reset_index()
    result = result.sort_values(["date"]).reset_index(drop=True)
    result["time_spent_cumsum"] = result.groupby(["dedicated_team_planning_period_id"])["time_spent"].cumsum(axis=0)

    return result

def propagate_dedicated_team_planning_period_planning_period_start_into_dedicated_team_planning_period_time_sheets_by_date(
        dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods
):
    dedicated_team_planning_periods_reduced_to_id_and_start = dedicated_team_planning_periods[["id", "planning_period_start"]].rename(columns={
        "id": "dedicated_team_planning_period_id",
    })

    return dedicated_team_planning_period_time_sheets_by_date.merge(
        dedicated_team_planning_periods_reduced_to_id_and_start,
        how="left",
        on="dedicated_team_planning_period_id",
        suffixes=(None, ""),
    )

def propagate_dedicated_team_planning_period_planning_period_end_into_dedicated_team_planning_period_time_sheets_by_date(
        dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods
):
    planning_periods_reduced_to_id_and_start = dedicated_team_planning_periods[["id", "planning_period_end"]].rename(columns={
        "id": "dedicated_team_planning_period_id",
    })

    return dedicated_team_planning_period_time_sheets_by_date.merge(
        planning_periods_reduced_to_id_and_start,
        how="left",
        on="dedicated_team_planning_period_id",
        suffixes=(None, ""),
    )

def calculate_dedicated_team_planning_period_time_spent_cumsum_prediction_by_dedicated_team_planning_periods_m_and_b(
        dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods
):
    dedicated_team_planning_periods_reduced_to_id_m_and_b = dedicated_team_planning_periods[["id", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]]
    result = dedicated_team_planning_period_time_sheets_by_date.merge(
        dedicated_team_planning_periods_reduced_to_id_m_and_b,
        how="left",
        left_on="dedicated_team_planning_period_id",
        right_on="id",
        suffixes=(None, "")
    )

    result["time_spent_cumsum_prediction"] = result.apply(lambda x:
        normalize(x=x["date"], min_x=x["planning_period_start"], max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
        axis=1
    )

    return result
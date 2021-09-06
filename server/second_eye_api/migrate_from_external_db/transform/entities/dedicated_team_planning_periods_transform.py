import pandas as pd
from ..utils import linear_polyfit

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

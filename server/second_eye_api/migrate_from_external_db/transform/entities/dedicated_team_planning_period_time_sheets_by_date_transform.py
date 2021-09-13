from ..utils import normalize

def calculate_dedicated_team_planning_period_time_spent_cumsum_prediction_by_dedicated_team_planning_periods_m_and_b(
        dedicated_team_planning_period_time_sheets_by_date,
        dedicated_team_planning_periods
):
    dedicated_team_planning_periods_reduced_to_id_m_and_b = dedicated_team_planning_periods[["id", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]]
    dedicated_team_planning_periods_reduced_to_id_m_and_b.set_index(["id"], inplace=True)
    result = dedicated_team_planning_period_time_sheets_by_date.merge(
        dedicated_team_planning_periods_reduced_to_id_m_and_b,
        how="left",
        left_on="dedicated_team_planning_period_id",
        right_index=True,
        suffixes=(None, "")
    )

    result["time_spent_cumsum_prediction"] = result.apply(lambda x:
        normalize(x=x["date"], min_x=x["planning_period_start"], max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
        axis=1
    )

    return result
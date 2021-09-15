from ..utils import normalize

def calculate_planning_period_time_spent_cumsum_prediction_by_planning_periods_m_and_b(
        planning_period_time_sheets_by_date,
        planning_periods
):
    planning_periods_reduced_to_id_m_and_b = planning_periods[["id", "time_sheets_by_date_model_m", "time_sheets_by_date_model_b"]]
    planning_periods_reduced_to_id_m_and_b.set_index("id", inplace=True)

    result = planning_period_time_sheets_by_date.merge(
        planning_periods_reduced_to_id_m_and_b,
        how="left",
        left_on="planning_period_id",
        right_index=True,
        suffixes=(None, "")
    )

    result["time_spent_cumsum_prediction"] = result.apply(lambda x:
        normalize(x=x["date"], min_x=x["planning_period_start"], max_x=x["planning_period_end"]) * x["time_sheets_by_date_model_m"] + x["time_sheets_by_date_model_b"],
        axis=1
    )

    return result